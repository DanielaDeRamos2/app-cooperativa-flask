def notificar_cliente(cliente, mensagem):
    # Simples: salvar em DB ou apenas print log
    print(f"[NOTIFICAÇÃO a {cliente.email}] {mensagem}")
