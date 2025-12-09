#!/usr/bin/env python
"""Test individual blueprint imports"""
import sys

print("Testing individual blueprint imports...\n")

blueprints_to_test = [
    ("auth", "app.blueprints.auth", "auth_bp"),
    ("categorias", "app.blueprints.categorias", "categorias_bp"),
    ("produtos", "app.blueprints.produtos", "produtos_bp"),
    ("pedidos", "app.blueprints.pedidos", "pedidos_bp"),
    ("carrinho", "app.blueprints.pedidos", "carrinho_bp"),
    ("produtores", "app.blueprints.produtores", "produtores_bp"),
    ("produtor_pedidos", "app.blueprints.produtores", "produtor_pedidos_bp"),
    ("admin_pedidos", "app.blueprints.admin", "admin_pedidos_bp"),
]

failed = []

for name, module, blueprint_var in blueprints_to_test:
    try:
        print(f"[{name:20}] Importing {module}...", end=" ")
        mod = __import__(module, fromlist=[blueprint_var])
        bp = getattr(mod, blueprint_var)
        print(f"✓ OK")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        failed.append((name, str(e)))
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
if failed:
    print(f"❌ {len(failed)} blueprint(s) failed to import:")
    for name, err in failed:
        print(f"  - {name}: {err}")
    sys.exit(1)
else:
    print("✅ All blueprints imported successfully!")
    sys.exit(0)
