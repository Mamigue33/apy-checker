#!/usr/bin/env python3
import socket, sys, ssl, time, os, urllib.request
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

os.system('clear')
print("\033[1;31m")
print("  ╔════════════════════════════════════════════════════════╗")
print("  ║                 APY@ CHECKER 😈  v3.0                  ║")
print("  ║           Domain | SNI Scanner | Top 3 Traffic         ║")
print("  ╚════════════════════════════════════════════════════════╝")
print("\033[0m")
print("\033[1;36m" + "="*60 + "\033[0m")
print("\033[1;33m          🔥 FERRAMENTA PROFISSIONAL 🔥\033[0m")
print("\033[1;36m" + "="*60 + "\033[0m\n")

def test_sni(domain):
    try:
        start = time.time()
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                lat = round((time.time()-start)*1000, 2)
                return {'domain': domain, 'lat': lat, 'status': 'ok', 'tls': ssock.version()}
    except:
        return {'domain': domain, 'status': 'no'}

def medir_trafego(domain):
    try:
        start = time.time()
        req = urllib.request.Request(f"https://{domain}/", headers={'User-Agent': 'APY@'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            dados = resp.read(50000)
            vel = (len(dados)*8)/((time.time()-start)*1024)
            return round(vel, 2)
    except:
        return 0

def scan(domain):
    subs = ['www', 'mail', 'api', 'blog', 'admin', 'dev', 'test', 'app', 'cloud', 'login', 'secure', 'cdn']
    snis = [domain] + [f"{s}.{domain}" for s in subs]
    print(f"\n📊 Analisando {len(snis)} SNIs...\n")
    resultados = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(test_sni, s): s for s in snis}
        for i, f in enumerate(as_completed(futures), 1):
            r = f.result()
            if r['status'] == 'ok':
                vel = medir_trafego(r['domain'])
                r['vel'] = vel
                r['score'] = round(max(0, 100 - r['lat']/10) + vel/10, 2)
                resultados.append(r)
                print(f"\033[32m[{i}/{len(snis)}] ✓ {r['domain']:<30} [{r['lat']}ms] [{vel}Kbps]\033[0m")
            else:
                print(f"\033[90m[{i}/{len(snis)}] ✗ {r['domain']:<30}\033[0m")
    resultados.sort(key=lambda x: x['score'], reverse=True)
    return resultados

try:
    op = input("\n\033[1;33m[1] Scan Completo [2] Top 3 [0] Sair: \033[0m").strip()
    if op == '0':
        print("\n\033[1;31mSaindo...\033[0m")
        sys.exit(0)
    alvo = input("\033[1;33m🌐 Domínio: \033[0m").strip()
    if not alvo:
        print("\033[1;31mInválido!\033[0m")
        sys.exit(1)
    resultados = scan(alvo)
    if resultados:
        print("\n\033[1;33m" + "="*50 + "\033[0m")
        print("\033[1;33m🏆 TOP 3 SNIs 🏆\033[0m")
        print("\033[1;33m" + "="*50 + "\033[0m")
        for i, r in enumerate(resultados[:3], 1):
            print(f"\n\033[1;33m{i}º - \033[1;37m{r['domain']}\033[0m")
            print(f"   📍 Latência: \033[32m{r['lat']}ms\033[0m")
            print(f"   📡 Velocidade: \033[32m{r.get('vel',0)} Kbps\033[0m")
            print(f"   🔒 TLS: \033[32m{r.get('tls','N/A')}\033[0m")
            print(f"   📊 Score: \033[33m{r['score']}/100\033[0m")
        nome = f"apy_{alvo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(nome, 'w') as f:
            f.write(f"<h1>APY@ Report</h1><p>{alvo}</p><p>{datetime.now()}</p><p>SNIs ativas: {len(resultados)}</p>")
        print(f"\n\033[32m✅ Relatório: {nome}\033[0m")
        print(f"\033[32m✅ Total SNIs ativas: {len(resultados)}\033[0m")
except KeyboardInterrupt:
    print("\n\033[31mInterrompido!\033[0m")
