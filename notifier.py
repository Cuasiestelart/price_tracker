import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_price_alert(product_name, current_price, target_price, product_url):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("[Notifier Error] Faltan variables de entorno en .env")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"¡Alerta de precio! {product_name} bajó a ${current_price:.2f}"
    msg["From"] = sender
    msg["To"] = receiver

    body = f"""
    ¡Buenas noticas! El producto que estás monitoreando alcanzó tu precio meta.

    procuto: {product_name}
    Precio actual: ${current_price:.2f} MXN
    Tu precio meta: ${target_price:.2f} MXN
    Enlace de compra:
    {product_url}
    """
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"[Notifier] Correo enviado exitosamente a {receiver}")
        return True
    except Exception as e:
        print(f"[Notifier Error] No se pudo enviar el correo: {e}")
        return False

# --- Bloque de prueba individual ---

if __name__ == "__main__":
    send_price_alert(
        product_name="Teclado ajazz AK820 Pro",
        current_price=699.00,
        target_price=700,
        product_url="https://ejemplo.com/producto"
    )

