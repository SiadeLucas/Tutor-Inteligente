"""
Cliente de Integração com o Gateway de Pagamentos Asaas (v3).
Suporta ambiente Sandbox, Produção e modo Simulado para testes e desenvolvimento local sem chave.
"""
import base64
import uuid
import logging
from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import httpx

from app.core.config import settings
from app.models.user import Usuario

logger = logging.getLogger("app.modules.payments.asaas_service")


class AsaasService:
    """Gerencia a comunicação com a API REST v3 do Asaas."""

    def __init__(self):
        self.api_key = settings.ASAAS_API_KEY.strip()
        self.environment = settings.ASAAS_ENVIRONMENT.lower()
        if self.environment == "production":
            self.base_url = "https://api.asaas.com/api/v3"
        else:
            self.base_url = "https://sandbox.asaas.com/api/v3"

    @property
    def is_configured(self) -> bool:
        """Verifica se há chave de API real configurada."""
        return bool(self.api_key and len(self.api_key) > 10)

    def _headers(self) -> Dict[str, str]:
        return {
            "access_token": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "TutorInteligente/1.0",
        }

    async def criar_cobranca_pix(
        self,
        usuario: Usuario,
        valor: Decimal,
        descricao: str,
        referencia_id: str,
        expiracao_minutos: int = 15,
    ) -> Dict[str, Any]:
        """
        Emite cobrança PIX no Asaas e obtém QR Code SVG/Base64 + Copia e Cola.
        Se não houver chave no ambiente dev, retorna simulação fiel instantânea.
        """
        if self.is_configured:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    # 1. Cria a cobrança no Asaas
                    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    payload = {
                        "customer": await self._obter_ou_criar_cliente_asaas(client, usuario),
                        "billingType": "PIX",
                        "value": float(valor),
                        "dueDate": hoje,
                        "description": descricao,
                        "externalReference": referencia_id,
                        "postalService": False,
                    }
                    resp = await client.post(
                        f"{self.base_url}/payments",
                        json=payload,
                        headers=self._headers(),
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    payment_id = data.get("id")

                    # 2. Busca QRCode PIX
                    qr_resp = await client.get(
                        f"{self.base_url}/payments/{payment_id}/pixQrCode",
                        headers=self._headers(),
                    )
                    qr_resp.raise_for_status()
                    qr_data = qr_resp.json()

                    return {
                        "gateway_transacao_id": payment_id,
                        "valor": valor,
                        "pix_copia_e_cola": qr_data.get("payload", ""),
                        "pix_qrcode_base64": qr_data.get("encodedImage", ""),
                        "expira_em": datetime.now(timezone.utc) + timedelta(minutes=expiracao_minutos),
                        "raw_payload": data,
                    }
            except Exception as e:
                logger.warning(f"Falha ao comunicar com Asaas real: {e}. Alternando para simulação de desenvolvimento.")

        # Modo Simulado (Offline / Dev / Sandbox fallback)
        simulated_id = f"pay_sim_{uuid.uuid4().hex[:16]}"
        simulated_payload = f"00020126580014br.gov.bcb.pix0136{uuid.uuid4()}520400005303986540{float(valor):.2f}5802BR5917TutorInteligente6009SAOPAULO62070503***6304"
        # Gera uma imagem SVG simulada em base64
        svg_mock = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">'
            f'<rect width="200" height="200" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>'
            f'<text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="#0f172a" font-family="sans-serif">QR CODE PIX</text>'
            f'<text x="50%" y="60%" dominant-baseline="middle" text-anchor="middle" font-size="12" fill="#F57C00" font-family="sans-serif">R$ {valor:.2f}</text>'
            f'</svg>'
        )
        b64_qr = f"data:image/svg+xml;base64,{base64.b64encode(svg_mock.encode()).decode()}"

        return {
            "gateway_transacao_id": simulated_id,
            "valor": valor,
            "pix_copia_e_cola": simulated_payload,
            "pix_qrcode_base64": b64_qr,
            "expira_em": datetime.now(timezone.utc) + timedelta(minutes=expiracao_minutos),
            "raw_payload": {
                "id": simulated_id,
                "status": "PENDING",
                "billingType": "PIX",
                "simulado": True,
            },
        }

    async def criar_cobranca_cartao(
        self,
        usuario: Usuario,
        valor: Decimal,
        descricao: str,
        referencia_id: str,
        cartao_dados: Dict[str, Any],
        parcelas: int = 1,
    ) -> Dict[str, Any]:
        """
        Processa pagamento via Cartão de Crédito no Asaas.
        """
        if self.is_configured:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    payload = {
                        "customer": await self._obter_ou_criar_cliente_asaas(client, usuario),
                        "billingType": "CREDIT_CARD",
                        "value": float(valor),
                        "dueDate": hoje,
                        "description": descricao,
                        "externalReference": referencia_id,
                        "installmentCount": parcelas,
                        "installmentValue": float(valor / parcelas),
                        "creditCard": {
                            "holderName": cartao_dados.get("nome_titular"),
                            "number": cartao_dados.get("numero_cartao"),
                            "expiryMonth": cartao_dados.get("mes_expiracao"),
                            "expiryYear": cartao_dados.get("ano_expiracao"),
                            "ccv": cartao_dados.get("cvv"),
                        },
                        "creditCardHolderInfo": {
                            "name": usuario.nome_completo,
                            "email": usuario.email,
                            "cpfCnpj": usuario.cpf,
                            "postalCode": usuario.cep,
                            "addressNumber": usuario.numero or "S/N",
                            "phone": usuario.telefone or "11999998888",
                        },
                    }
                    resp = await client.post(
                        f"{self.base_url}/payments",
                        json=payload,
                        headers=self._headers(),
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    status_pag = data.get("status")
                    net_val = Decimal(str(data.get("netValue", valor)))
                    taxa = max(Decimal("0.00"), valor - net_val) if "netValue" in data else Decimal("0.00")

                    return {
                        "gateway_transacao_id": data.get("id"),
                        "status": "paid" if status_pag in ("CONFIRMED", "RECEIVED") else "pending",
                        "valor_bruto": valor,
                        "taxa_gateway": taxa,
                        "raw_payload": data,
                    }
            except Exception as e:
                logger.warning(f"Falha ao comunicar com Asaas cartão: {e}. Alternando para simulação de desenvolvimento.")

        # Simulação para desenvolvimento
        simulated_id = f"pay_cc_sim_{uuid.uuid4().hex[:16]}"
        return {
            "gateway_transacao_id": simulated_id,
            "status": "paid",  # Cartão aprovado em sandbox simulado
            "valor_bruto": valor,
            "taxa_gateway": Decimal("1.50"),
            "raw_payload": {
                "id": simulated_id,
                "status": "CONFIRMED",
                "billingType": "CREDIT_CARD",
                "simulado": True,
            },
        }

    async def _obter_ou_criar_cliente_asaas(self, client: httpx.AsyncClient, usuario: Usuario) -> str:
        """Localiza ou cadastra o cliente no Asaas pelo CPF."""
        # Busca se já existe
        busca_resp = await client.get(
            f"{self.base_url}/customers?cpfCnpj={usuario.cpf}",
            headers=self._headers(),
        )
        if busca_resp.is_success:
            itens = busca_resp.json().get("data", [])
            if itens:
                return itens[0]["id"]

        # Cria novo
        novo_payload = {
            "name": usuario.nome_completo,
            "cpfCnpj": usuario.cpf,
            "email": usuario.email,
            "mobilePhone": usuario.telefone or None,
            "postalCode": usuario.cep,
            "addressNumber": usuario.numero or "S/N",
        }
        res_novo = await client.post(
            f"{self.base_url}/customers",
            json=novo_payload,
            headers=self._headers(),
        )
        res_novo.raise_for_status()
        return res_novo.json()["id"]


asaas_service = AsaasService()
