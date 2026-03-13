import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")

def enviar_alerta(nome, preco_atual, preco_alvo, url):
    assunto = f"🚨 Alerta de preço: {nome}"

    corpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
        <div style="background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: auto;">
            <h2 style="color: #2ecc71;">✅ Preço abaixo do alvo!</h2>
            <p style="font-size: 1.1rem;">O produto <strong>{nome}</strong> atingiu o preço desejado.</p>
            <table style="width:100%; margin-top: 20px;">
                <tr>
                    <td style="color: #888;">Preço atual</td>
                    <td style="font-size: 1.5rem; color: #2ecc71;"><strong>£{preco_atual}</strong></td>
                </tr>
                <tr>
                    <td style="color: #888;">Preço alvo</td>
                    <td><strong>£{preco_alvo}</strong></td>
                </tr>
            </table>
            <a href="{url}" style="display:inline-block; margin-top:24px; padding: 12px 24px;
               background:#2ecc71; color:white; border-radius:8px; text-decoration:none;
               font-weight:bold;">Ver produto</a>
        </div>
    </body>
    </html>
    """

    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = assunto
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINATARIO
    mensagem.attach(MIMEText(corpo, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, mensagem.as_string())
        print(f"  📧 E-mail enviado para {EMAIL_DESTINATARIO}")
    except Exception as e:
        print(f"  ❌ Erro ao enviar e-mail: {e}")