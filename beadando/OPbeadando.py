import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Szoba:
    def __init__(self, ar, szobaszam, tipus):
        self.ar = ar
        self.szobaszam = szobaszam
        self.tipus = tipus  # Tipus: 'Egyágyas' vagy 'Ketagyas'

    def __str__(self):
        return f"{self.tipus} Szoba, Szobaszám: {self.szobaszam}, Ár: {self.ar}"

class Foglalas:
    def __init__(self, szoba, datum, foglalo_nev):
        self.szoba = szoba
        self.datum = datum
        self.foglalo_nev = foglalo_nev

    def __str__(self):
        return f"Foglalt szoba: {self.szoba.szobaszam}, Foglalva: {self.datum}, Foglaló: {self.foglalo_nev}"

class Szalloda:
    def __init__(self):
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def szoba_foglalas(self, szobaszam, datum, foglalo_nev):
        foglalasi_datum = datetime.strptime(datum, "%Y-%m-%d")
        if foglalasi_datum <= datetime.now():
            raise ValueError("A foglalást csak jővőbeli időpontra lehetséges.")
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if any(foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum for foglalas in self.foglalasok):
                    raise Exception(f"A szoba ({szobaszam}) már foglalt ezen a dátumon ({datum}).")
                foglalas = Foglalas(szoba, datum, foglalo_nev)
                self.foglalasok.append(foglalas)
                return f"Foglalás megtörtént: {szoba}"
        raise ValueError("Nincs ilyen szobaszámú szoba.")

    def foglalas_lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return f"Foglalás lemondva: Szoba {szobaszam}, Dátum {datum}"
        return "Nem található foglalás ezzel a szobaszámmal és dátummal."

    def szoba_lista(self):
        return '\n'.join(str(szoba) for szoba in self.szobak)

    def lefoglalt_szobak_listazasa(self):
        if not self.foglalasok:
            return "Jelenleg nincsenek foglalások."
        else:
            return '\n'.join(str(foglalas) for foglalas in self.foglalasok)

class SzallodaApp:
    def __init__(self, master):
        self.master = master
        self.szalloda = Szalloda()
        self.setup_szalloda()

        master.title("Szálloda Rendszer")

        tk.Label(master, text="Üdvözöljük a szálloda rendszerében!").pack()

        tk.Button(master, text="Szoba foglalása", command=self.szoba_foglalas).pack()
        tk.Button(master, text="Foglalás lemondása", command=self.foglalas_lemondas).pack()
        tk.Button(master, text="Szobák listázása", command=self.szoba_lista).pack()
        tk.Button(master, text="Lefoglalt szobák listázása", command=self.lefoglalt_szobak_listazasa).pack()
        tk.Button(master, text="Kilépés", command=master.quit).pack()

    def setup_szalloda(self):
        # Szobák hozzáadása
        self.szalloda.szoba_hozzaadas(Szoba(15000, "1", "Egyágyas"))
        self.szalloda.szoba_hozzaadas(Szoba(20000, "2", "Kétágyas"))
        self.szalloda.szoba_hozzaadas(Szoba(18000, "3", "Egyágyas"))
        self.szalloda.szoba_hozzaadas(Szoba(22000, "4", "Kétágyas"))
        self.szalloda.szoba_hozzaadas(Szoba(16000, "5", "Egyágyas"))

        # Foglalások előre definiálása
        self.szalloda.szoba_foglalas("1", "2024-07-20", "Bocskai Csenge")
        self.szalloda.szoba_foglalas("2", "2024-06-15", "Nagy Ferenc")
        self.szalloda.szoba_foglalas("3", "2024-07-01", "Fehér Péter")
        self.szalloda.szoba_foglalas("2", "2024-08-10", "Gyöztes Zsombor")
        self.szalloda.szoba_foglalas("5", "2024-09-05", "Szemere Bertalan")

    def szoba_foglalas(self):
        szobaszam = simpledialog.askstring("Foglalás", "Szobaszám:")
        datum = simpledialog.askstring("Foglalás", "Dátum (éééé-hh-nn):")
        foglalo_nev = simpledialog.askstring("Foglalás", "Foglaló neve:")
        try:
            eredmeny = self.szalloda.szoba_foglalas(szobaszam, datum, foglalo_nev)
            messagebox.showinfo("Foglalás", eredmeny)
        except Exception as e:
            messagebox.showerror("Foglalási Hiba", str(e))

    def foglalas_lemondas(self):
        szobaszam = simpledialog.askstring("Lemondás", "Szobaszám:")
        datum = simpledialog.askstring("Lemondás", "Dátum (éééé-hh-nn):")
        eredmeny = self.szalloda.foglalas_lemondas(szobaszam, datum)
        messagebox.showinfo("Lemondás", eredmeny)

    def szoba_lista(self):
        eredmeny = self.szalloda.szoba_lista()
        messagebox.showinfo("Szobák Listája", eredmeny)

    def lefoglalt_szobak_listazasa(self):
        eredmeny = self.szalloda.lefoglalt_szobak_listazasa()
        messagebox.showinfo("Lefoglalt Szobák", eredmeny)

if __name__ == "__main__":
    root = tk.Tk()
    app = SzallodaApp(root)
    root.mainloop()
