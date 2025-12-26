import sys
from colorama import Fore, Style, init
from .email_dfa import EmailDFAWithCounter

init(autoreset=True)

def main():
    validator = EmailDFAWithCounter(on_step=lambda cur, ch, nxt: print(
        f"{Style.DIM}δ({cur}, '{ch if ch is not None else '∅'}') -> {nxt}{Style.RESET_ALL}"
    ))

    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Masukkan email: ").strip()

    print(f"Memvalidasi: {email}")
    is_valid = validator.validate(email)

    if is_valid:
        print(Fore.GREEN + "Valid ✅")
    else:
        print(Fore.RED + "Tidak valid ❌")

if __name__ == "__main__":
    main()
