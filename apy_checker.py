#!/usr/bin/env python3
import socket, sys, ssl, time, os, urllib.request
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def clear():
    os.system('clear')

def banner():
    clear()
    print("\033[1;31m")
    print("  ╔══════════════════════════════════════════════════════════════════╗")
    print("  ║                    APY@ CHECKER 😈  v4.0                         ║")
    print("  ║           Scanner Profissional | SNI | Domínios | IP             ║")
    print("  ╚══════════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    print("\033[1;36m" + "=" * 70 + "\033[0m")
    print("\033[1;33m              🔥 FERRAMENTA COMPLETA DE ANÁLISE 🔥\033[0m")
    print("\033[1;36m" + "=" * 70 + "\033[0m\n")

def menu():
    print("\033[1;36m╔════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║                         📋 MENU PRINCIPAL 📋                     ║\033[0m")
    print("\033[1;36m╠════════════════════════════════════════════════════════════════╣\033[0m")
    print("\033[1;33m║  [1] 🔍 Scanner de Domínios                                     ║\033[0m")
    print("\033[1;36m║  [2] 🌐 Scanner de Múltiplas SNI                                ║\033[0m")
    print("\033[1;35m║  [3] 📡 Scanner de IP Address                                   ║\033[0m")
    print("\033[1;33m║  [4] 📊 Scanner de Tráfego de SNI                               ║\033[0m")
    print("\033[1;36m║  [5] 🔎 Pesquisar Lista de SNI Online                           ║\033[0m")
    print("\033[1;35m║  [6] 🐌 Scanner de SlowDNS                                      ║\033[0m")
    print("\033[1;33m║  [7] 🔗 Scanner de SNI Associadas                               ║\033[0m")
    print("\033[1;36m║  [8] 🌍 Scanner de Internet da SNI                              ║\033[0m")
    print("\033[1;35m║  [9] 🏆 Testar Várias SNI + Top 3 + Tráfego                     ║\033[0m")
    print("\033[1;33m║  [10] 💾 Download de Lista de SNI                               ║\033[0m")
    print("\033[1;31m║  [0] ❌ Sair                                                    ║\033[0m")
    print("\033[1;36m╚════════════════════════════════════════════════════════════════╝\033[0m")

def scan_dominios():
    print("\n\033[1;34m🔍 SCANNER DE DOMÍNIOS\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio base: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Domínio inválido!\033[0m")
        return
    subs = ['www', 'mail', 'ftp', 'dev', 'api', 'blog', 'admin', 'test']
    print(f"\n📊 Escaneando {len(subs)} subdomínios...\n")
    for sub in subs:
        alvo = f"{sub}.{dominio}"
        try:
            ip = socket.gethostbyname(alvo)
            print(f"\033[32m✓ {alvo:<35} -> {ip}\033[0m")
        except:
            print(f"\033[90m✗ {alvo:<35}\033[0m")

def scan_slowdns():
    print("\n\033[1;34m🐌 SCANNER DE SLOWDNS\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    subs = ['ns1', 'ns2', 'dns1', 'dns2', 'ns', 'dns']
    print(f"\n📊 Testando SlowDNS para {dominio}...\n")
    for sub in subs:
        alvo = f"{sub}.{dominio}"
        try:
            start = time.time()
            socket.gethostbyname(alvo)
            tempo = round((time.time() - start) * 1000, 2)
            if tempo > 500:
                print(f"\033[33m⚠️ {alvo:<35} -> {tempo}ms (LENTO)\033[0m")
            else:
                print(f"\033[32m✓ {alvo:<35} -> {tempo}ms\033[0m")
        except:
            print(f"\033[90m✗ {alvo:<35}\033[0m")

def main():
    banner()
    menu()
    try:
        opcao = input("\n\033[1;33m👉 Escolha uma opção: \033[0m").strip()
        if opcao == '0':
            print("\n\033[1;31m❌ Saindo... Até mais! 👋\033[0m")
            return
        elif opcao == '1':
            scan_dominios()
        elif opcao == '6':
            scan_slowdns()
        else:
            print("\n\033[1;33m📌 Funcionalidade em desenvolvimento!\033[0m")
            print("\033[1;33m👉 Opções disponíveis: 1 (Domínios) e 6 (SlowDNS)\033[0m")
        input("\n\033[1;33m\n👉 Pressione ENTER para continuar...\033[0m")
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m❌ Programa interrompido!\033[0m")
    except EOFError:
        print("\n\033[1;31m❌ Entrada inválida! Execute novamente.\033[0m")

if __name__ == "__main__":
    main()
