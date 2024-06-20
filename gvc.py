from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QRegExpValidator, QIcon
from datetime import datetime
import time
from numba import jit

from PyQt5.QtCore import QTimer, Qt, QRegExp, QUrl
from functools import partial
from random import randint
import random
import sqlite3
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os
import csv
start = time.time()
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class GVC:
    def __init__(self):
        # Load App
        self.App = QApplication([])

        # Interfaces
        self.Dashboard = loadUi(resource_path("gui/gas.ui"))
        self.ajouterProduit = loadUi(resource_path("gui/new_product.ui"))
        self.deleteStock = loadUi(resource_path("gui/supprime.ui"))
        self.quantityDiag = loadUi(resource_path("gui/quantity_diag.ui"))
        self.codeAccess = loadUi(resource_path("gui/auth.ui"))
        self.quantityDiag2 = loadUi(resource_path("gui/quantity_diag2.ui"))
        self.stockWidget = QWidget()
        self.OldRef = ""

        self.clicked_text = ""  # Initialize a variable to store clicked text

        self.button_connections = {} # Store button connections

        # Window
        self.Dashboard.setFixedSize(1920, 1080)  # Set fixed size
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))

        # Connection

        

        self.Connection = sqlite3.connect("stock.db")
        self.Cursor = self.Connection.cursor()
        self.Cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_reference ON stock(reference)"
        )
        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock (
            nom TEXT,
            description TEXT,
            prix REAL,
            quantite TEXT,
            reference TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        """
        create_rec_query = """
        CREATE TABLE IF NOT EXISTS rec (
            id TEXT,
            recettes TEXT
        )
        """
        self.Cursor.execute(create_table_query)
        self.Cursor.execute(create_rec_query)

        # Recettes
        self.ConnectionRec = sqlite3.connect("recettes.db")
        self.CursorRec = self.ConnectionRec.cursor()
        self.CursorRec.execute("CREATE INDEX IF NOT EXISTS idx_reference ON rec(id)")

        # Timer

        self.timerDate = QTimer()
        

        
        
        self.timerLabel = QTimer()
        
        
        self.rowCount = 0
        self.colnames = [
            self.Dashboard.stock.horizontalHeaderItem(col).text() for col in range(5)
        ]
        self.Dashboard.rech.focusInEvent = self.buttonAcces

        # Table
        self.Dashboard.stock.itemSelectionChanged.connect(self.get_selected_rows)

        # Button
        self.caisseButton = self.Dashboard.caisseAjoute
        self.caisseButton.setEnabled(False)
        self.caisseButton.clicked.connect(self.handleCaisse)


        
        # Caisse
        self.Montant = self.Dashboard.montant

        reg_ex = QRegExp(
            "[0-9]+(\\.[0-9]+)?"
        )  # This regex matches any number with up to 9 digits
        input_validator = QRegExpValidator(reg_ex, self.Montant)

        self.Montant.setValidator(input_validator)
        self.ListVCaisse = self.Dashboard.caisseache
        self.Receipt = self.Dashboard.receipt
        self.Cancel_items = self.Dashboard.cancel_all
        self.Cancel_one_item = self.Dashboard.cancel_one
        self.Checkout = self.Dashboard.checkout
        self.Montant.setEnabled(False)
        self.ListVCaisse.setEnabled(False)
        self.Receipt.setEnabled(False)
        self.Checkout.setEnabled(False)
        self.Cancel_items.setEnabled(False)
        self.Cancel_one_item.setEnabled(False)
        self.getCash = 0.0

        self.Total = 0.0
        self.Rem = 0.0
        self.AllItems = []
        self.indexItems = []
        self.RecList = []

        # Diag
        self.quantityDiag2.decline2.clicked.connect(self.on_decline2)
        self.quantityDiag.accept.clicked.connect(self.on_accept)
        self.quantityDiag.decline.clicked.connect(self.on_decline)

        # License
        act1 = self.Dashboard.menuLicence.addAction("Loi d'utilisation")
        act1.triggered.connect(self.show_eula)

        act2 = self.Dashboard.menuHelp.addAction("Fondateur")
        act2.triggered.connect(self.aboutApp)
        #
        self.selectionGlobal = []
        self.buttons = []
        self.buttonsInfo = []
        self.buttonsIndex = []
        self.add_items()
        self.selectedItems2 = []
        
        
    
    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())


    def aboutApp(self):
        about = """Saifeddine Makhlouf, développeur expérimenté depuis 3 ans, crée des logiciels innovants avec passion et précision. Toujours à la pointe de la technologie, il offre des solutions logicielles performantes et conviviales.

        """
        QMessageBox.information(self.Dashboard, "A propos", about, QMessageBox.Ok)



    def update_label(self):
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))
        self.Dashboard.ti.update()
    
    def deleteAll(self):
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))

        self.query = "DELETE FROM stock"
        reply = QMessageBox.question(self.Dashboard, "Confirmation", 
                                     "Êtes-vous sûr de vouloir supprimer tous les éléments de la table ?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.Cursor.execute(self.query)
            self.Connection.commit()
            
            reply = QMessageBox.information(self.Dashboard, "Information", 
                                     "Tous les éléments sont supprimé avec succés", 
                                     QMessageBox.Ok)
            self.Dashboard.stock.setRowCount(0)
            self.appendtotable()
            self.appendtotable_adm()
            self.clear_layout(self.Dashboard.itemsemb)
        else:
            pass


    
    def updater(self):
        self.clear_layout(self.Dashboard.itemsemb)
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))
        self.Dashboard.ti.update()
        self.Dashboard.stock.clearContents()
        self.Dashboard.stockadm.clearContents()
        self.appendtotable()
        self.appendtotable_adm()
        self.add_items()
        self.show_sold()
        
        self.stock_updater()
    def update_date(self):
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y | %H:%M:%S")
        self.Dashboard.fdate.setText("Date: " + date_str)
        self.timerDate.start(1000)
    
    def add_items(self):
         # Get the number of rows in the QTableWidget
        row_count = self.Dashboard.stock.rowCount()

        # Iterate over each row
        for row in range(row_count):
            # Get the QTableWidgetItem from each cell in the current row
            nom_item = self.Dashboard.stock.item(row, 0)
            description_item = self.Dashboard.stock.item(row, 1)
            prix_item = self.Dashboard.stock.item(row, 2)
            quantite_item = self.Dashboard.stock.item(row, 3)
            reference_item = self.Dashboard.stock.item(row, 4)
            
            # Check if any of the items is None
            if None in (nom_item, description_item, prix_item, quantite_item, reference_item):
                # Skip this row if any item is None
                continue

            # Get data from each cell in the current row
            nom = nom_item.text()
            description = description_item.text()
            prix = prix_item.text()
            quantite = quantite_item.text()
            reference = reference_item.text()

            # Create a QPushButton with the item data
            button_text = f"{nom}\n{description}\n{prix}\n{quantite}\n{reference}"
            button = QPushButton(button_text)
            self.buttons.append(button)

            # Add the button to the layout
            row_position = len(self.buttons) - 1
            row_index = row_position // 4
            col_index = row_position % 4
            self.Dashboard.itemsemb.addWidget(button, row_index, col_index)
            

        # Add buttons to the layout row-wise
        row = 0  # Start with the first row
        col = 0  # Start with the first column
        counter = 0
        for button in self.buttons:
            self.Dashboard.itemsemb.addWidget(button, row, col)
           

            button.setStyleSheet(f"margin: 5px;\n"
                                "color: black;\n"
                                    "padding:15px;\n"
                                    "text-align: center;\n"
                                    "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #D3D3D3, stop:1 #FFFFFF);\n"
                                    "font-size: 15px;"
                                    "border-style: solid;"
                                    "border-width: 2px;"
                                    "border-color: black;"
                                    "border-radius: 5px;")
            
            col += 1  # Move to the next column
            if col == 4:
                col = 0   # Reset column index to 0 for the next row
                row += 1  # Move to the next row
            connection = button.clicked.connect(partial(self.ItemsClickedButton, button.text()))
            self.button_connections[button] = connection  # Store the connection with the button
        self.buttons = []
        

    def ItemsClickedButton(self,button):
        self.clicked_text = button.split('\n')
        if(self.clicked_text[3]== 'HORS STOCK'):

            QMessageBox.critical(self.quantityDiag2,"Erreur","Le produit est hors stock !",QMessageBox.Ok)
        else:
            self.quantityDiag2.show()
            self.quantityDiag2.currentQuanta2.setText(
                "Quantité totale : " + str(self.clicked_text[3]))
            
            self.quantityDiag2.accept2.clicked.connect(partial(self.on_accept2,self.clicked_text))
            self.clicked_text = []
        
        
    def on_accept2(self,index):
        self.quantityDiag2.accept2.disconnect()
        quantity = self.quantityDiag2.quanta2.text().strip()
        if quantity > "0":
            self.selectedItems2 = index
            if self.Montant.text() == "0":
                self.Montant.setText("0")
                self.getCash = 0.0
                self.Rem = 0.0
            elif self.Montant.text() > "0":
                self.caisseButton.setEnabled(True)
                self.Rem = self.getCash - self.Total
                self.Receipt.setItem(
                    1, 0, QTableWidgetItem(str(self.truncate_float(float(self.Rem))))
                )
            
            checkedItem2 = []
            for item in self.selectedItems2:
                if item is not None:
                    checkedItem2.append(item)
                    
            self.selectedItems2 =[]
                    
                    

            
                    
            
            print("------->",checkedItem2)
            if int(quantity) < 0 or int(quantity) > int(checkedItem2[3]):
                QMessageBox.critical(
                    self.quantityDiag2,
                    "Erreur",
                    f"Le quantité {quantity} n'est pas valide ou insuffisante",
                )
            else:
                self.quantityDiag.close()
                if checkedItem2 is not None:
                    self.Total += float(checkedItem2[2].replace("DT","")) * int(
                        quantity
                    )
                self.Montant.setEnabled(True)
                self.ListVCaisse.setEnabled(True)
                self.Receipt.setEnabled(True)
                self.Cancel_items.setEnabled(True)
                self.Cancel_one_item.setEnabled(True)
                self.Checkout.setEnabled(False)

                self.Receipt.setColumnCount(1)
                self.Receipt.horizontalHeader().setVisible(False)
                self.Receipt.horizontalHeader().setSectionResizeMode(
                    QHeaderView.Stretch
                )

                self.TotalItem = QTableWidgetItem(str(float(self.Total)))  # create the item
                self.TotalItem.setTextAlignment(Qt.AlignHCenter)  # change the alignmen

                self.RemItem = QTableWidgetItem(
                    str(self.Rem)
                )  # create the item
                self.RemItem.setTextAlignment(Qt.AlignHCenter)  # change the alignmen

                self.Receipt.setItem(0, 0, QTableWidgetItem(self.TotalItem))
                self.Receipt.setItem(1, 0, QTableWidgetItem(self.RemItem))

                self.itemVariables = ""
                self.itemTuple = ()

                for i, name in enumerate(checkedItem2):
                    self.itemTuple += (name,)
                checkedItem2 = []
                nom, desc, prix, quant, ref = self.itemTuple
                now = datetime.now()

                self.Date = now.strftime("%d/%m/%Y %H:%M:%S")

                self.itemVariables += (
                    "Date : "
                    + self.Date
                    + "\n-------------------------\nNom : "
                    + str(nom)
                    + "\n Quantité : "
                    + str(quantity)
                    + "\n Prix Unitaire : "
                    + str(prix)
                    + "\n Reference : "
                    + str(ref)
                    + "\n---------------------------"
                )
                self.newTuple = (
                    nom,
                    int(quantity),
                    float(str(prix).replace(" DT", "")),
                    ref,
                )
                self.AllItems.append(self.newTuple)

                self.ListVCaisse.addItem(self.itemVariables)
                self.itemVariables = ""
                checkedItem2 = []
                self.selectedItems = ()
                
                
                
        else:
            QMessageBox.critical(
                self.quantityDiag,
                "Erreur",
                "La quantité doit etre remplit et superieur a zero",
            )
        
        self.button_connections.clear()  # Clear the stored connections dictionary
        self.quantityDiag2.close()
        self.add_items()
        
    def on_decline2(self):
        self.quantityDiag2.close()

    def show_eula(self):
        eula_text = """
        CONTRAT DE LICENCE UTILISATEUR FINAL (CLUF)

        IMPORTANT : VEUILLEZ LIRE ATTENTIVEMENT CE CONTRAT DE LICENCE UTILISATEUR FINAL AVANT D'UTILISER CE LOGICIEL.

       CONTRAT DE LICENCE UTILISATEUR FINAL (CLUF)

        IMPORTANT : VEUILLEZ LIRE ATTENTIVEMENT CE CONTRAT DE LICENCE UTILISATEUR FINAL AVANT D'UTILISER CE LOGICIEL.

        1. DÉFINITIONS :
        a. "Logiciel" désigne le programme informatique fourni en vertu du présent Contrat de Licence Utilisateur Final.
        b. "Développeur" ou "Fournisseur" désigne le créateur original et propriétaire du Logiciel.
        c. "Utilisateur" désigne toute personne physique ou morale qui acquiert le droit d'utiliser le Logiciel en vertu de cet accord.

        2. OCTROI DE LICENCE :
        a. Sous réserve des termes et conditions du présent Contrat, le Développeur accorde à l'Utilisateur une licence non exclusive et non transférable pour utiliser le Logiciel.
        b. L'Utilisateur peut utiliser le Logiciel uniquement à des fins personnelles ou internes à l'entreprise et ne peut pas distribuer, vendre, concéder sous licence ou transférer autrement le Logiciel à un tiers.

        3. RESTRICTIONS :
        a. L'Utilisateur ne peut pas modifier, adapter, traduire, désassembler ou décompiler le Logiciel en tout ou en partie.
        b. L'Utilisateur ne peut pas supprimer ou modifier les avis de copyright, de marque déposée ou autres avis de propriété contenus dans ou sur le Logiciel.
        c. L'Utilisateur ne peut pas utiliser le Logiciel à des fins illégales ou non autorisées.

        4. FRAIS DE LICENCE :
        a. L'Utilisateur accepte de payer les frais de licence applicables au Développeur en échange du droit d'utiliser le Logiciel.
        b. L'Utilisateur reconnaît que le non-paiement des frais de licence peut entraîner la résiliation de la licence et des poursuites judiciaires par le Développeur.

        5. EXCLUSION DE GARANTIE :
        LE LOGICIEL EST FOURNI "TEL QUEL" SANS AUCUNE GARANTIE, EXPRESSE OU IMPLICITE. LE DÉVELOPPEUR EXCLUT TOUTES LES GARANTIES, Y COMPRIS, MAIS SANS S'Y LIMITER, LA QUALITÉ MARCHANDE, L'ADÉQUATION À UN USAGE PARTICULIER ET LA NON-CONTREFAÇON.

        6. LIMITATION DE RESPONSABILITÉ :
        LE DÉVELOPPEUR NE SERA EN AUCUN CAS RESPONSABLE DES DOMMAGES INDIRECTS, ACCESSOIRES, SPÉCIAUX, EXEMPLAIRES OU CONSÉCUTIFS DÉCOULANT DE L'UTILISATION OU DE L'INCAPACITÉ D'UTILISER LE LOGICIEL, MÊME SI LE DÉVELOPPEUR A ÉTÉ AVISÉ DE LA POSSIBILITÉ DE TELS DOMMAGES. EN AUCUN CAS LA RESPONSABILITÉ TOTALE DU DÉVELOPPEUR NE DÉPASSERA LE MONTANT PAYÉ PAR L'UTILISATEUR POUR LE LOGICIEL.

        7. LOI APPLICABLE :
        Le présent Contrat sera régi et interprété conformément aux lois de [Juridiction], sans égard à ses règles de conflit de lois.

        8. RÉSILIATION :
        Le présent Contrat prendra fin automatiquement si l'Utilisateur ne respecte pas l'une quelconque des modalités ou conditions du présent Contrat. À la résiliation, l'Utilisateur cessera toute utilisation du Logiciel et détruira toutes les copies du Logiciel en sa possession ou sous son contrôle.

        9. INTÉGRALITÉ DE L'ACCORD :
        Le présent Contrat constitue l'intégralité de l'accord entre l'Utilisateur et le Développeur concernant l'objet des présentes et remplace tous les accords ou ententes antérieurs ou contemporains, écrits ou oraux, concernant ledit objet.

        EN UTILISANT LE LOGICIEL, L'UTILISATEUR RECONNAÎT AVOIR LU ET COMPRIS CE CONTRAT ET ACCEPTE D'ÊTRE LIÉ PAR SES TERMES ET CONDITIONS.



        EN UTILISANT LE LOGICIEL, L'UTILISATEUR RECONNAÎT AVOIR LU ET COMPRIS CE CONTRAT ET ACCEPTE D'ÊTRE LIÉ PAR SES TERMES ET CONDITIONS.
        """

        QMessageBox.information(self.Dashboard, "Licence", eula_text, QMessageBox.Ok)
     
    def show_sold(self):
        
        self.Dashboard.listrec.clear()
        rec_query = "SELECT * FROM rec"
        self.CursorRec.execute(rec_query)
        self.rows = self.CursorRec.fetchall()
        temp = ""
        self.getSum = 0.0
        self.getTotal = ""
        self.getQuantityTotal = ""
        self.sumQuantity = 0
        self.Rem = ""
        self.sumRem = 0
        for row in self.rows:
            if len(row) > 1:
                temp += (
                    "ID de Recette : "
                    + row[0]
                    + "\n\n-----------------------\n"
                    + row[1]
                )
                self.Dashboard.listrec.addItem(temp)
                temp = ""
                self.getTotal = str(row[1])
                self.getQuantityTotal = str(row[1])
                self.Rem = str(row[1])
                if (
                    str(row[1]).find("Totale:") != -1
                    and str(row[1]).find("Monnaie:") != -1
                    and str(row[1]).find("---------------------------------") != -1
                ):
                    self.getTotal = float(
                        self.getTotal[
                            str(row[1]).find("Totale:")
                            + len("Totale:") : str(row[1]).find("Monnaie:")
                        ].strip()
                    )
                    self.getSum += float(self.getTotal)
                    self.getQuantityTotal = (
                        self.getQuantityTotal[
                            str(row[1])
                            .find("---------------------------------") : str(row[1])
                            .find("x")
                        ]
                        .strip()
                        .replace("---------------------------------", "")
                    )
                    self.sumQuantity += int(self.getQuantityTotal)
                    self.Rem = self.Rem[
                        str(row[1]).find("Monnaie:") : len(self.Rem)
                    ].strip()
                    self.Rem = self.Rem.split(" ")
                    self.Rem = (
                        self.Rem.pop(1)
                        .strip()
                        .replace("---------------------------------", "")
                        .strip()
                    )
                    self.sumRem += float(self.Rem)

        self.Dashboard.dataRec.clear()
        self.Dashboard.dataRec.addItem(
            f"Totale quantité vendu: {str(self.sumQuantity)}\nSomme de tout produit vendu: {str(self.truncate_float(float(self.getSum - self.sumRem)))} DT"
        )

        self.Dashboard.rech_rec.textChanged.connect(self.handleSearchRec)
    
    def handleSearchRec(self):
        self.input = str(self.Dashboard.rech_rec.text())
        temp = ""
        if self.input != "":
            
            self.Dashboard.listrec.clear()
            search_query = f"""
            SELECT * FROM rec WHERE
            id LIKE '%{self.input}%' OR
            recettes LIKE '%{self.input}%'
            """
            self.CursorRec.execute(search_query)
            self.rows = self.CursorRec.fetchall()

            for row in self.rows:
                temp += (
                    "ID de Recette : "
                    + row[0]
                    + "\n\n-----------------------\n"
                    + row[1]
                )
                self.Dashboard.listrec.addItem(temp)
                temp = ""
        else:
            self.Dashboard.listrec.clear()
            self.show_sold()
            

        self.Dashboard.listrec.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.Dashboard.listrec.setMinimumSize(self.Dashboard.listrec.sizeHint())

        # Set the model for the list view

    def truncate_float(self, float_number):
        # Convert the float to a string and split it at the decimal point
        integer_part, fractional_part = str(float_number).split(".")

        # Truncate the fractional part to two digits
        truncated_fractional_part = fractional_part[:2]

        # Join the integer part and truncated fractional part with a decimal point
        truncated_float_string = f"{integer_part}.{truncated_fractional_part}"

        # Convert the truncated string back to a float
        truncated_float = float(truncated_float_string)

        return truncated_float
    
    def show_dashboard(self):
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))

        self.codeAccess.show()
        self.appendtotable()
        self.appendtotable_adm()
        self.stock_updater()
        self.show_sold()
        self.update_date()
        self.add_items()
        self.admtablefilter()
        self.Dashboard.ajoute.clicked.connect(self.show_add_product)
        self.Dashboard.modifier.clicked.connect(self.modify_stock)
        self.Dashboard.supprime.clicked.connect(self.delete_stock)
        self.deleteStock.sprbtn.clicked.connect(self.confirm_delete)
        self.Dashboard.itemsGas.currentChanged.connect(self.on_tab_changed)
        self.Dashboard.ajoutmasse.clicked.connect(self.add_batch_file)
        self.Dashboard.deleteall.clicked.connect(self.deleteAll)
        self.timerDate.timeout.connect(self.update_date)
        
        self.timerLabel.timeout.connect(self.update_label)
        
        self.timerLabel.start(1000)
        


        
        # Other vars

        # self.timer.timeout.connect(self.appendtotable)
        # self.timer.start(3000)

        # 8self.timerAdm.timeout.connect(self.appendtotable_adm)
        # self.timerAdm.start(3000)

        self.Dashboard.rech.textChanged.connect(self.search_query)
        self.Dashboard.rech2.textChanged.connect(self.search_query2)

        self.Dashboard.montant.textChanged.connect(self.constraint_montant)
        self.quantityDiag.quanta.textChanged.connect(self.constraint_diag)
        self.ListVCaisse.itemSelectionChanged.connect(self.on_item_selection_changed)

        self.Cancel_items.clicked.connect(self.cancel_all_items)
        self.Cancel_one_item.clicked.connect(self.cancel_one_item)
        self.Checkout.clicked.connect(self.checkout)
        self.codeAccess.accepter.clicked.connect(self.authentication_use_tab)

        self.currIndexTab = self.Dashboard.itemsGas.currentIndex()
        self.player = QMediaPlayer()
        self.Dashboard.itemsGas.setTabEnabled(3, False)
        # Load the audio file
        audio_path = (
            "gui/sound/sound.mp3"  # Replace "example.mp3" with the path to your audio file
        )
        audio_url = QUrl.fromLocalFile(audio_path)  # Create QUrl from local file path
        audio_content = QMediaContent(audio_url)  # Create QMediaContent from QUrl
        self.player.setMedia(audio_content)  # Set media content

        # Play the audio
        self.player.play()



    def add_batch_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self.Dashboard, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the header row
                for idx, row in enumerate(csv_reader, start=2):  # start counting rows from 2 (1-based index)
                    try:
                        nom = str(row[0])
                        description = str(row[1])
                        prix = float(row[2])
                        quantite = int(row[3])
                        reference = str(row[4])

                        # Check if reference exists in the database
                        self.Cursor.execute("SELECT COUNT(*) FROM stock WHERE reference=?", (reference,))
                        count = self.Cursor.fetchone()[0]
                        if count > 0:
                            print(f"Reference {reference} already exists. Skipping row {idx}")
                            continue

                        # If reference does not exist, insert the row into the database
                        self.query = "INSERT INTO stock(nom, description, prix, quantite, reference) VALUES (?, ?, ?, ?, ?)"
                        self.Cursor.execute(self.query, (nom, description, prix, quantite, reference))
                        self.Connection.commit()
                        print(f"Inserted row {idx}: {nom}, {description}, {prix}, {quantite}, {reference}")

                    except (IndexError, ValueError) as e:
                        print(f"Error in row {idx}: {e}")
                        continue
                    
            QMessageBox.information(self.Dashboard, "Information", "Les articles ont été ajoutés avec succès")
            self.Dashboard.stock.clearContents()
            self.Dashboard.stockadm.clearContents()
            self.add_items()
            self.appendtotable()
            self.appendtotable_adm()
            self.show_sold()
            self.stock_updater()
            
            self.stock_updater()
            self.updater()

        else:
            QMessageBox.information(self.Dashboard, "Erreur", "Les articles n'ont pas été ajoutés")


    def authentication_use_tab(self):
        self.code = self.codeAccess.codeD.text()

        # Check if the code is incorrect
        if self.code != "chef" and self.code != "emp":
            QMessageBox.information(
                self.deleteStock, "Information", "Le code d'accès est incorrect."
            )

        # If the code is 'chef', show the Dashboard and disable specific tabs
        if self.code == "chef":
            self.Dashboard.show()
            self.Dashboard.itemsGas.setTabEnabled(3, True)
            self.Dashboard.itemsGas.setTabEnabled(1, True)
            self.codeAccess.close()

        # If the code is 'emp', show the Dashboard and disable specific tabs
        if self.code == "emp":
            self.Dashboard.show()
            self.Dashboard.itemsGas.setTabEnabled(3, False)
            self.Dashboard.itemsGas.setTabEnabled(1, False)
            self.codeAccess.close()

    def on_item_selection_changed(self):
        selected_indexes = self.ListVCaisse.selectedIndexes()
        selected_items = [index.row() for index in selected_indexes]

        if selected_items is not None or len(selected_items) != 0:
            self.indexItems = selected_items

        else:
            self.indexItems = []

    def cancel_one_item(self):
        self.selected_item = self.ListVCaisse.currentItem()

        if self.selected_item is not None:
            row = self.ListVCaisse.row(self.selected_item)
            self.ListVCaisse.takeItem(row)

            if len(self.AllItems) > 0 and len(self.indexItems) == 1:
                if self.getCash > 0.0:
                    if self.indexItems:
                        self.Rem = self.getCash - (
                            self.Total
                            - float(self.AllItems[self.indexItems[0]][2])
                            * float(self.AllItems[self.indexItems[0]][1])
                        )
                        self.Total -= float(
                            self.AllItems[self.indexItems[0]][2]
                        ) * float(self.AllItems[self.indexItems[0]][1])
                        self.Receipt.setItem(0, 0, QTableWidgetItem(str(self.Total)))
                        self.Receipt.setItem(
                            1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
                        )
                        self.AllItems.pop(self.indexItems[0])
                else:
                    if self.indexItems:
                        self.Rem = 0.0
                        self.Total -= float(
                            self.AllItems[self.indexItems[0]][2]
                        ) * float(self.AllItems[self.indexItems[0]][1])
                        self.Receipt.setItem(0, 0, QTableWidgetItem(str(self.Total)))
                        self.Receipt.setItem(
                            1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
                        )
                        self.AllItems.pop(self.indexItems[0])

        if not self.ListVCaisse.count():
            self.AllItems = []
            self.indexItems = []
            self.Cancel_items.setCheckable(False)
            self.Cancel_one_item.setCheckable(False)
            self.Montant.setEnabled(False)
            self.ListVCaisse.setEnabled(False)
            self.Receipt.setEnabled(False)
            self.Cancel_items.setEnabled(False)
            self.Cancel_one_item.setEnabled(False)
            self.Checkout.setEnabled(False)
            self.Receipt.setItem(0, 0, QTableWidgetItem(str(0.0)))
            self.Receipt.setItem(1, 0, QTableWidgetItem(str(0.0)))
        else:
            self.indexItems = []

    def cancel_all_items(self):
        self.ListVCaisse.clear()
        self.indexItems = []
        self.getCash = 0.0
        self.Rem = 0.0
        self.Total = 0.0
        self.Receipt.setItem(0, 0, QTableWidgetItem(str(0.0)))
        self.Receipt.setItem(1, 0, QTableWidgetItem(str(0.0)))
        self.Cancel_items.setCheckable(False)
        self.Cancel_one_item.setCheckable(False)

        if self.ListVCaisse.count() == 0:
            self.AllItems = []
            self.indexItems = []
            self.Montant.setEnabled(False)
            self.ListVCaisse.setEnabled(False)
            self.Receipt.setEnabled(False)
            self.Cancel_items.setEnabled(False)
            self.Cancel_one_item.setEnabled(False)
            self.Checkout.setEnabled(False)
            self.Cancel_items.setCheckable(False)
            self.Cancel_one_item.setCheckable(False)

    def constraint_montant(self):
        input = self.Montant.text()

        if input == "0":
            self.Montant.setText("0")
            self.getCash = 0.0
            self.Rem = 0.0
            self.Receipt.setItem(
                1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
            )
        elif input == "":
            self.Montant.setText("")
            self.getCash = 0.0
            self.Rem = 0.0
            self.Receipt.setItem(
                1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
            )

        if input > "0":
            if float(input) < self.Total:
                self.Checkout.setEnabled(False)
            else:
                self.Checkout.setEnabled(True)
                self.getCash = float(input)
                self.Rem = float(self.getCash) - self.Total
                self.Receipt.setItem(
                    1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
                )

    def constraint_diag(self):
        input = self.quantityDiag.quanta.text()
        if not str(input).isdecimal():
            self.quantityDiag.quanta.setText("0")
        if input == "":
            self.quantityDiag.quanta.setText("0")

    def appendtotable(self):
        query_update = """
        UPDATE stock
        SET quantite="HORS STOCK"
        WHERE quantite=0
        """
        self.Cursor.execute(query_update)
        self.Connection.commit()  # Commit the transaction
        query = "SELECT nom, description, prix, quantite, reference FROM stock ORDER BY quantite ASC"

        self.Cursor.execute(query)
        self.Rows = self.Cursor.fetchall()

        for row in range(len(self.Rows)):
            self.Dashboard.stock.setRowCount(len(self.Rows))
            index = 0

            self.Dashboard.stock.setItem(
                row, 0, QTableWidgetItem(str(self.Rows[row][0]))
            )
            self.Dashboard.stock.setItem(
                row, 1, QTableWidgetItem(str(self.Rows[row][1]))
            )
            self.Dashboard.stock.setItem(
                row, 2, QTableWidgetItem(str(self.Rows[row][2]) + " DT")
            )

            self.Dashboard.stock.setItem(
                row, 3, QTableWidgetItem(str(self.Rows[row][3]))
            )
            self.Dashboard.stock.setItem(
                row, 3, QTableWidgetItem(str(self.Rows[row][3]))
            )
            self.Dashboard.stock.setItem(
                row, 4, QTableWidgetItem(str(self.Rows[row][4]))
            )
            
            self.Dashboard.stock.setVerticalHeaderItem(row, QTableWidgetItem(""))

            index += 1
            self.rowCount += 1
    
    def appendtotable_adm(self):
        
        query_update = """
        UPDATE stock
        SET quantite="HORS STOCK"
        WHERE quantite=0
        """
        self.Cursor.execute(query_update)
        self.Connection.commit()  # Commit the transaction

        query = "SELECT nom, description, prix, quantite, reference FROM stock ORDER BY quantite ASC"
        self.Cursor.execute(query)
        rows = self.Cursor.fetchall()

        self.Dashboard.stockadm.clearContents()  # Clear existing contents

        # Set the number of rows and columns in the table
        self.Dashboard.stockadm.setRowCount(len(rows))
        self.Dashboard.stockadm.setColumnCount(5)  # Assuming there are 5 columns

        # Set horizontal header labels and resize columns
        headers = ["Nom", "Description", "Prix", "Quantité", "Référence"]
        self.Dashboard.stockadm.setHorizontalHeaderLabels(headers)
        self.Dashboard.stockadm.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # Populate the table with data from the database
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.Dashboard.stockadm.setItem(row_index, col_index, item)
                self.Dashboard.stockadm.setVerticalHeaderItem(row_index, QTableWidgetItem(""))

        # Disable the modifier button initially
        self.Dashboard.modifier.setEnabled(False)

        # Connect the selectionChanged signal to the handleSelection method
        self.Dashboard.stockadm.selectionModel().selectionChanged.connect(
            self.handleSelection
        )
        self.Dashboard.ti.setText(str("Produit en totale --> " + str(self.Dashboard.stock.rowCount())))
    
    def admtablefilter(self):
        self.Dashboard.quantitefiltre.textChanged.connect(self.apply_filter)
        self.Dashboard.reffiltre.textChanged.connect(self.apply_filter)
        self.Dashboard.prixcroitfiltre.stateChanged.connect(self.apply_filter)
        self.Dashboard.prixdecroitfiltre.stateChanged.connect(self.apply_filter)
        self.Dashboard.quantitecroit.stateChanged.connect(self.apply_filter)
        self.Dashboard.quantitedecroit.stateChanged.connect(self.apply_filter)
    
    def apply_filter(self):
        # Get the filter criteria from the UI components
        search_quantite = self.Dashboard.quantitefiltre.text()
        search_reference = self.Dashboard.reffiltre.text()
        prix_croissant = self.Dashboard.prixcroitfiltre.isChecked()
        prix_decroissant = self.Dashboard.prixdecroitfiltre.isChecked()
        quantite_croissant = self.Dashboard.quantitecroit.isChecked()
        quantite_decroissant = self.Dashboard.quantitedecroit.isChecked()

        # Check if all filters are empty
        all_filters_empty = not any([search_quantite, search_reference, prix_croissant, prix_decroissant, quantite_croissant, quantite_decroissant])

        # Ensure only one of the quantity sorting checkboxes is checked
        if quantite_croissant or quantite_decroissant:
            self.Dashboard.prixcroitfiltre.setEnabled(False)
            self.Dashboard.prixdecroitfiltre.setEnabled(False)
        else:
            self.Dashboard.prixcroitfiltre.setEnabled(True)
            self.Dashboard.prixdecroitfiltre.setEnabled(True)

        # Ensure only one of the price sorting checkboxes is checked
        if prix_croissant or prix_decroissant:
            self.Dashboard.quantitecroit.setEnabled(False)
            self.Dashboard.quantitedecroit.setEnabled(False)
        else:
            self.Dashboard.quantitecroit.setEnabled(True)
            self.Dashboard.quantitedecroit.setEnabled(True)

        # Construct the SQL query based on the active filter criteria
        if all_filters_empty:
            query = "SELECT * FROM stock"
        else:
            query = "SELECT * FROM stock WHERE 1=1"

        params = []

        if search_quantite:
            query += " AND quantite LIKE ?"
            params.append(f"%{search_quantite}%")

        if search_reference:
            query += " AND reference LIKE ?"
            params.append(f"%{search_reference}%")

        if prix_croissant:
            query += " ORDER BY prix ASC"
        elif prix_decroissant:
            query += " ORDER BY prix DESC"

        if quantite_croissant:
            query += " ORDER BY quantite ASC"
        elif quantite_decroissant:
            query += " ORDER BY quantite DESC"

        # Execute the query with parameters
        self.Cursor.execute(query, params)
        rows = self.Cursor.fetchall()

        # Clear existing contents
        self.Dashboard.stockadm.clearContents()

        # Set the number of rows and columns in the table
        self.Dashboard.stockadm.setRowCount(len(rows))
        self.Dashboard.stockadm.setColumnCount(5)  # Assuming there are 5 columns

        # Set horizontal header labels and resize columns
        headers = ["Nom", "Description", "Prix", "Quantité", "Référence"]
        self.Dashboard.stockadm.setHorizontalHeaderLabels(headers)
        self.Dashboard.stockadm.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with data from the database
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.Dashboard.stockadm.setItem(row_index, col_index, item)

        # Reset original state if all filters are removed
        if all_filters_empty:
            self.Dashboard.prixcroitfiltre.setEnabled(True)
            self.Dashboard.prixdecroitfiltre.setEnabled(True)
            self.Dashboard.quantitecroit.setEnabled(True)
            self.Dashboard.quantitedecroit.setEnabled(True)



    
    def select_all_from_stock(self):
        # Perform SELECT * FROM stock query
        self.Cursor.execute("SELECT * FROM stock")
        rows = self.Cursor.fetchall()

        # Clear existing contents
        self.Dashboard.stockadm.clearContents()

        # Set the number of rows and columns in the table
        self.Dashboard.stockadm.setRowCount(len(rows))
        self.Dashboard.stockadm.setColumnCount(5)  # Assuming there are 5 columns

        # Set horizontal header labels and resize columns
        headers = ["Nom", "Description", "Prix", "Quantité", "Référence"]
        self.Dashboard.stockadm.setHorizontalHeaderLabels(headers)
        self.Dashboard.stockadm.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with data from the database
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.Dashboard.stockadm.setItem(row_index, col_index, item)

# Other helper methods for enabling/disabling sorting checkboxes as before


    
    def handleSelection(self):
        selected_items = self.Dashboard.stockadm.selectedItems()
        self.selectionGlobal = selected_items
        if selected_items:
            # Assuming you want to handle only the first selected item
            selected_row = selected_items[
                0
            ].row()  # Get the row index of the selected item
            num_columns = (
                self.Dashboard.stockadm.columnCount()
            )  # Get the number of columns

            row_text = []
            for col in range(num_columns):
                item = self.Dashboard.stockadm.item(
                    selected_row, col
                )  # Get the QTableWidgetItem
                text = (
                    item.text() if item else ""
                )  # Get the text of the item or an empty string if it's None
                row_text.append(text)

            self.selectionGlobal = row_text
            self.Dashboard.modifier.clicked.connect(self.modify_stock)
            self.Dashboard.modifier.setEnabled(True)
        else:
            self.selectionGlobal = []
            self.Dashboard.modifier.setEnabled(False)
    
    def search_query(self):
        self.caisseButton.setEnabled(False)
        search_term = self.Dashboard.rech.text()
        if search_term != "":
            self.Dashboard.stock.clearContents()
            self.Dashboard.stock.setRowCount(0)
            query = f"""
            SELECT * 
            FROM stock 
            WHERE nom LIKE '%{search_term}%' 
            OR description LIKE '%{search_term}%' 
            OR prix LIKE '%{search_term}%' 
            OR quantite LIKE '%{search_term}%' 
            OR reference LIKE '%{search_term}%'
            """

            self.Cursor.execute(query)
            self.Rows = self.Cursor.fetchall()

            for row in range(len(self.Rows)):
                self.Dashboard.stock.setRowCount(len(self.Rows))
                index = 0

                self.Dashboard.stock.setItem(
                    row, 0, QTableWidgetItem(str(self.Rows[row][0]))
                )
                self.Dashboard.stock.setItem(
                    row, 1, QTableWidgetItem(str(self.Rows[row][1]))
                )
                self.Dashboard.stock.setItem(
                    row, 2, QTableWidgetItem(str(self.Rows[row][2]) + " DT")
                )
                self.Dashboard.stock.setItem(
                    row, 3, QTableWidgetItem(str(self.Rows[row][3]))
                )
                self.Dashboard.stock.setItem(
                    row, 4, QTableWidgetItem(str(self.Rows[row][4]))
                )
                index += 1

        else:
            self.appendtotable()
            self.show_sold()
            

    def update_cols(self):
        self.colnames = [
            self.Dashboard.stock.horizontalHeaderItem(col).text() for col in range(5)
        ]
    
    def search_query2(self):
        search_term = (
            self.Dashboard.rech2.text().strip()
        )  # Get the search term from the QLineEdit
        query = ""
        if search_term:  # Check if the search term is not empty
            # Construct the SQL query with the search term
            query = f"""
            SELECT * 
            FROM stock 
            WHERE nom LIKE '%{search_term}%' 
            OR description LIKE '%{search_term}%' 
            OR prix LIKE '%{search_term}%' 
            OR quantite LIKE '%{search_term}%' 
            OR reference LIKE '%{search_term}%'
            """
        else:
            # If the search term is empty, select all rows
            query = "SELECT nom, description, prix, quantite, reference FROM stock"
            self.show_sold()

        # Execute the query
        self.Cursor.execute(query)
        rows = self.Cursor.fetchall()

        # Clear the existing contents of the QTableWidget
        self.Dashboard.stockadm.clearContents()

        # Set the number of rows and columns in the table
        self.Dashboard.stockadm.setRowCount(len(rows))
        self.Dashboard.stockadm.setColumnCount(5)  # Assuming there are 5 columns

        # Populate the table with data from the database
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.Dashboard.stockadm.setItem(row_index, col_index, item)

    def check_alpha(self, string):
        for i in range(len(string)):
            if string[i] < "A" or string[i] > "Z":
                return False

        if len(string) == 0:
            return False
        return True
    
    def addProduct(self):
        self.inputs = [
            str(self.ajouterProduit.add_nom.text()),
            str(self.ajouterProduit.add_desc.text()),
            str(self.ajouterProduit.add_prix.text()),
            str(self.ajouterProduit.add_quant.text()),
            str(self.ajouterProduit.add_ref.text()),
        ]

        existence = f"SELECT * FROM stock WHERE reference = ?"
        self.Cursor.execute(existence, (self.inputs[4],))
        getRef = self.Cursor.fetchone()

        if getRef is not None:
            QMessageBox.critical(
                self.ajouterProduit, "Erreur", "La référence existe déjà"
            )
            allValid = False
        else:
            allValid = True  # Assume all inputs are valid initially
            for i, input_value in enumerate(self.inputs):
                if i == 0 and not input_value:
                    QMessageBox.critical(
                        self.ajouterProduit, "Erreur", "Le nom ne doit pas être vide"
                    )
                    allValid = False
                elif i == 1 and not input_value:
                    QMessageBox.critical(
                        self.ajouterProduit,
                        "Erreur",
                        "La description ne doit pas être vide",
                    )
                    allValid = False
                elif i == 2:
                    try:
                        prix = float(input_value)
                        if prix < 0:
                            raise ValueError
                    except ValueError:
                        QMessageBox.critical(
                            self.ajouterProduit,
                            "Erreur",
                            "Le prix doit être un nombre positif",
                        )
                        allValid = False
                elif i == 3:
                    try:
                        quantite = int(input_value)
                        if quantite < 0:
                            raise ValueError
                    except ValueError:
                        QMessageBox.critical(
                            self.ajouterProduit,
                            "Erreur",
                            "La quantité doit être un entier positif",
                        )
                        allValid = False
                elif i == 4 and not input_value:
                    QMessageBox.critical(
                        self.ajouterProduit,
                        "Erreur",
                        "La référence ne doit pas être vide",
                    )
                    allValid = False

        if allValid:
            data = (
                self.inputs[0],
                self.inputs[1],
                self.inputs[2],
                self.inputs[3],
                self.inputs[4],
            )
            query = f"INSERT INTO stock(nom, description, prix, quantite, reference) VALUES (?,?,?,?,?)"

            self.Cursor.execute(query, data)
            self.Connection.commit()  # Commit the transaction
            QMessageBox.information(
                self.ajouterProduit,
                "Information",
                "Le produit a été ajouté avec succès",
            )
            self.ajouterProduit.close()
            self.appendtotable()
            self.appendtotable_adm()
            self.show_sold()
            self.buttonsInfo = []
            self.add_items()
            self.ajouterProduit.add_nom.setText("")
            self.ajouterProduit.add_desc.setText("")
            self.ajouterProduit.add_prix.setText("")
            self.ajouterProduit.add_quant.setText("")
            self.ajouterProduit.add_ref.setText("")

    def show_add_product(self):
        self.ajouterProduit.show()
        self.ajouterProduit.addProd.clicked.connect(self.addProduct)
    
    def modify_stock(self):
        self.stockWidget.setWindowTitle("Modifier le stock d'un produit")
        try:
            self.stockWidget.setGeometry(
                500 // 2 + 700 // 2, 700 // 2, 500, 700
            )  # Set the position and size of the widget
        except ZeroDivisionError:
            pass

        self.gridLayout = QFormLayout()
        self.stockWidget.setFixedSize(500, 300)  # Set width and height of the widget
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(
            True
        )  # Allow the scroll area to resize its widget
        self.stockWidget.setLayout(
            self.gridLayout
        )  # Set a vertical layout for the main widget

        column_names = [
            self.Dashboard.stock.horizontalHeaderItem(col).text() for col in range(5)
        ]

        self.gridLayout.setSpacing(5)  # Set spacing between items to 10 pixels

        # Add column labels and line edits for each row
        for i in range(1):
            for j in range(5):  # Exclude the reference column
                label = QLabel(column_names[j])
                lineEdit = QLineEdit()
                lineEdit.setObjectName(
                    f"s_{i}_{j}"
                )  # Assign a unique name based on row and column index
                self.gridLayout.addRow(
                    label, lineEdit
                )  # Add label and line edit to the layout

                # Populate QLineEdit with data from row_data
                if i < len(self.selectionGlobal) and j < 5:
                    lineEdit.setText(str(self.selectionGlobal[j]))

            # Add button for saving changes
            saveButton = QPushButton("Save")
            saveButton.setObjectName(
                f"saveButton_{i}"
            )  # Assign a unique name for each button
            saveButton.clicked.connect(
                partial(self.saveChanges, saveButton)
            )  # Pass the sender button as an argument
            self.gridLayout.addWidget(saveButton)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            self.gridLayout.addRow(line)

            self.stockWidget.show()
        self.OldRef = self.selectionGlobal[4]
    
    def saveChanges(self, button):
        button_name = button.objectName()  # Get the name of the button
        row_index = int(
            button_name.split("_")[1]
        )  # Extract the row index from the button name

        # Get the line edits for the corresponding row and extract the data
        row_data = []
        for j in range(5):
            lineEdit = self.stockWidget.findChild(QLineEdit, f"s_{row_index}_{j}")
            if lineEdit:
                row_data.append(lineEdit.text())

        queryd = "SELECT id  FROM stock WHERE reference = ?"
        self.Cursor.execute(queryd, (self.OldRef,))
        id = self.Cursor.fetchone()[0]


        # Check if row_data has enough elements
        if len(row_data) == 5:
            # Update the database with the modified data
            query = f"UPDATE stock SET nom = ?, description = ?, prix = ?, quantite = ? , reference = ? WHERE id = ?"
            self.Cursor.execute(
                query,
                (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], id),
            )
            self.Connection.commit()  # Commit the transaction

            # Optionally, you can display a message to indicate that the changes were saved
            QMessageBox.information(
                self.stockWidget, "Information", "Modifié avec succés."
            )
            self.appendtotable_adm()
            self.appendtotable()
            self.stock_updater()
            self.show_sold()
            self.add_items()
            self.stockWidget.close()
            self.OldRef = ""

        else:
            QMessageBox.warning(
                self.stockWidget, "Warning", "Les donnés de la ligne sont erroné"
            )
    
    def delete_stock(self):
        if not self.deleteStock.isVisible():
            self.deleteStock.show()
            self.stock_updater()
        else:
            self.stock_updater()
    
    def stock_updater(self):
        self.deleteStock.itemsTable.clear()
        query = "SELECT nom, description, prix, quantite, reference FROM stock"
        self.Cursor.execute(query)
        self.Rows = self.Cursor.fetchall()
        row_data = []
        aux = ""
        for row in range(len(self.Rows)):
            for j in range(len(self.colnames)):
                aux += f"{self.colnames[j]} : {self.Rows[row][j]}\n"
            self.deleteStock.itemsTable.addItem(aux)

            aux = ""
        self.deleteStock.rech3.textChanged.connect(self.delete_rech)
    
    def delete_rech(self):
        search = self.deleteStock.rech3.text()
        aux = ""

        if str(search) == "":
            self.deleteStock.itemsTable.clear()
            query = "SELECT nom, description, prix, quantite, reference FROM stock"
            self.Cursor.execute(query)
            self.Rows = self.Cursor.fetchall()
            row_data = []
            aux = ""
            for row in range(len(self.Rows)):
                for j in range(len(self.colnames)):
                    aux += f"{self.colnames[j]} : {self.Rows[row][j]}\n"
                self.deleteStock.itemsTable.addItem(aux)

                aux = ""
        else:
            self.deleteStock.itemsTable.clear()

            query = f"""
            SELECT * 
            FROM stock 
            WHERE nom LIKE '%{search}%' 
            OR description LIKE '%{search}%' 
            OR prix LIKE '%{search}%' 
            OR quantite LIKE '%{search}%' 
            OR reference LIKE '%{search}%'
            """

            self.Cursor.execute(query)
            self.Rows = self.Cursor.fetchall()

            for row in range(len(self.Rows)):
                self.deleteStock.itemsTable.addItem(
                    f"Nom : {str(self.Rows[row][0])}\nDescription : {str(self.Rows[row][1])}\nPrix : {str(self.Rows[row][2])}\nQuantité : {str(self.Rows[row][3])}\nReference : {str(self.Rows[row][4])}\n"
                )
    
    def confirm_delete(self):
        selected_items = self.deleteStock.itemsTable.selectedItems()

        if selected_items:
            # Display a message if an item is selected
            selected_item_text = selected_items[0].text()
            QMessageBox.information(
                self.deleteStock,
                "Information",
                f"La valeur selectionné: \n{selected_item_text} \n a été supprimé avec succés",
            )
            popRef = str(selected_item_text).split(":")
            x = popRef[5].strip()
            query = f"DELETE FROM stock WHERE reference = ?"
            self.Cursor.execute(query, (str(x),))
            self.Connection.commit()
            self.appendtotable()
            self.appendtotable_adm()
            self.show_sold()
            self.stock_updater()
            self.add_items()

        else:
            # Display a message if no item is selected
            QMessageBox.information(
                self.deleteStock, "Pas de selection", "Pas de valeur selectionné."
            )
    
    def buttonAcces(self, event):
        self.caisseButton.setEnabled(False)
        self.Dashboard.rech.setFocus()
        self.Dashboard.stock.clearSelection()
        self.selectedItems = self.Dashboard.stock.selectedItems()
        self.selectedItems = []
    
    def get_selected_rows(self):
        self.selectedItems = self.Dashboard.stock.selectedItems()
        selected_rows = set()
        self.getItems = []
        self.quantity = 0
        for item in self.selectedItems:
            if item is not None:
                self.caisseButton.setEnabled(True)
                self.getItems.append(item.text())

            else:
                self.caisseButton.setEnabled(False)
        for item in self.selectedItems:
            self.quantity = self.getItems[3]
            if str(self.getItems[3]) == "HORS STOCK":
                self.caisseButton.setEnabled(False)

        self.quantityDiag.currentQuanta.setText(
            "Quantité totale : " + str(self.quantity)
        )
    
    def on_tab_changed(self):
        self.caisseButton.setEnabled(False)
        self.Dashboard.stock.clearSelection()
        selection_model = self.Dashboard.stockadm.selectionModel()
        selection_model.clearSelection()
        self.ItemsList = self.Dashboard.stock.selectedItems()
        self.ItemsList = []
        self.indexItems = []
        if self.getCash > 0:
            self.Rem = self.getCash - self.Total
            self.Receipt.setItem(
                1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
            )
        else:
            self.Rem = 0.0
            self.Receipt.setItem(
                1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
            )

    def handleCaisse(self):
        self.quantityDiag.show()
    
    def on_accept(self):
        quantity = self.quantityDiag.quanta.text().strip()
        if quantity > "0":
            self.selectedItems = self.Dashboard.stock.selectedItems()
            checkedItem = []
            if self.Montant.text() == "0":
                self.Montant.setText("0")
                self.getCash = 0.0
                self.Rem = 0.0
            elif self.Montant.text() > "0":
                self.caisseButton.setEnabled(True)
                self.Rem = self.getCash - self.Total
                self.Receipt.setItem(
                    1, 0, QTableWidgetItem(str(self.truncate_float(self.Rem)))
                )
            else:
                self.caisseButton.setEnabled(False)
            for item in self.selectedItems:
                if item is not None:
                    self.caisseButton.setEnabled(True)
                    checkedItem.append(item.text())

                else:
                    self.caisseButton.setEnabled(False)

            if int(quantity) < 0 or int(quantity) > int(checkedItem[3]):
                QMessageBox.critical(
                    self.deleteStock,
                    "Erreur",
                    f"Le quantité {quantity} n'est pas valide ou insuffisante",
                )
            else:
                self.quantityDiag.close()
                if checkedItem is not None:
                    self.Total += float(checkedItem[2].replace(" DT", "")) * int(
                        quantity
                    )
                self.Montant.setEnabled(True)
                self.ListVCaisse.setEnabled(True)
                self.Receipt.setEnabled(True)
                self.Cancel_items.setEnabled(True)
                self.Cancel_one_item.setEnabled(True)
                self.Checkout.setEnabled(False)

                self.Receipt.setColumnCount(1)
                self.Receipt.horizontalHeader().setVisible(False)
                self.Receipt.horizontalHeader().setSectionResizeMode(
                    QHeaderView.Stretch
                )

                self.TotalItem = QTableWidgetItem(str(self.Total))  # create the item
                self.TotalItem.setTextAlignment(Qt.AlignHCenter)  # change the alignmen

                self.RemItem = QTableWidgetItem(
                    str(self.truncate_float(self.Rem))
                )  # create the item
                self.RemItem.setTextAlignment(Qt.AlignHCenter)  # change the alignmen

                self.Receipt.setItem(0, 0, QTableWidgetItem(self.TotalItem))
                self.Receipt.setItem(1, 0, QTableWidgetItem(self.RemItem))

                self.itemVariables = ""
                self.itemTuple = ()

                for i, name in enumerate(checkedItem):
                    self.itemTuple += (name,)

                nom, desc, prix, quant, ref = self.itemTuple
                now = datetime.now()

                self.Date = now.strftime("%d/%m/%Y %H:%M:%S")

                self.itemVariables += (
                    "Date : "
                    + self.Date
                    + "\n-------------------------\nNom : "
                    + str(nom)
                    + "\n Quantité : "
                    + str(quantity)
                    + "\n Prix Unitaire : "
                    + str(prix)
                    + "\n Reference : "
                    + str(ref)
                    + "\n---------------------------"
                )
                self.newTuple = (
                    nom,
                    int(quantity),
                    float(str(prix).replace(" DT", "")),
                    ref,
                )
                self.AllItems.append(self.newTuple)
                self.ListVCaisse.addItem(self.itemVariables)
                self.itemVariables = ""
                checkedItem = []
        else:
            QMessageBox.critical(
                self.quantityDiag,
                "Erreur",
                "La quantité doit etre remplit et superieur a zero",
            )

    def on_decline(self):
        self.quantityDiag.close()
    
    def counter(self, lst):
        # Initialize an empty dictionary to store the counts and total quantity for each item name
        counts = {}

        # Iterate through each tuple in the list
        for tup in lst:
            # Get the item name and quantity from the tuple
            item_name = tup[0]
            quantity = tup[1]

            # Convert item name to lowercase for case-insensitive counting
            item_name_lower = item_name

            # If the item name is already in the dictionary, increment its count and update total quantity
            if item_name_lower in counts:
                counts[item_name_lower]["count"] += 1
                counts[item_name_lower]["sum"] += quantity
            # If the item name is not in the dictionary, add it with count 1 and initial total quantity
            else:
                counts[item_name_lower] = {"count": 1, "sum": quantity}

        # Return the dictionary containing the counts and total quantities for each item name
        return counts
    
    def checkout(self):
        now = datetime.now()
        self.Date = now.strftime("%d/%m/%Y %H:%M:%S")

        self.ReceiptList = (
            "Date : " + self.Date + "\n---------------------------------\n"
        )
        for i in range(len(self.AllItems)):
            sql_get_quantity = "SELECT quantite FROM stock WHERE  reference = ?"
            self.Cursor.execute(sql_get_quantity, (str(self.AllItems[i][3]),))
            self.getQuantity = self.Cursor.fetchone()[0]
            sql_update_query = """UPDATE stock
                            SET quantite = ?
                            WHERE reference = ?"""
            self.Cursor.execute(
                sql_update_query,
                (
                    int(self.getQuantity) - int(self.AllItems[i][1]),
                    str(self.AllItems[i][3]),
                ),
            )
            self.Connection.commit()

        self.appendtotable()

        self.appendtotable_adm()
        self.stock_updater()
        self.ID = ""
        for i in range(1, 10):
            self.ID += str(randint(0, i + 5)) + chr(randint(0, i + 5) + 97)

        # Count occurrences of each item in AllItems

        item_counts = self.counter(
            [(item[0], item[1]) for item in self.AllItems]
        )  # Assuming quantity is at index 1

        for item_name, info in item_counts.items():
            total_quantity = info["sum"]
            print
            # Retrieve item information from the database based on its name
            sql_get_item = "SELECT nom, prix, reference FROM stock WHERE nom = ?"  # Assuming 'nom' is the item name column
            self.Cursor.execute(sql_get_item, (item_name,))
            item_info = self.Cursor.fetchone()

            # Append item details to the receipt
            self.ReceiptList += f"{total_quantity} x {item_info[0]} --\n"
            self.ReceiptList += (
                f"       >>Prix: {item_info[1]}\n       >>Ref: {item_info[2]}\n"
            )
            self.ReceiptList += (
                "---------------------------------\n"  # Separator between items
            )

        self.ReceiptList += (
            "\n\nN° Transaction >> "
            + self.ID
            + "XX"
            + "\n\nTotale: "
            + str(self.Total)
            + "\n\nMonnaie: "
            + str(self.truncate_float(float(self.getCash - self.Total)))
            + "\n---------------------------------"
        )

        final_query = "INSERT INTO rec VALUES (?,?)"
        self.CursorRec.execute(final_query, (self.ID, self.ReceiptList))
        self.ConnectionRec.commit()
        self.show_sold()
        self.cancel_all_items()
        self.print_string(self.ReceiptList)
        self.add_items()
        self.Montant.setText("0")

    def print_string(self, text):
        doc = QTextDocument()
        doc.setPlainText(text)

        # Create a QPrinter
        printer = QPrinter()

        # Create a QPrintDialog to choose printer settings
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Print the document
            doc.print_(printer)
end = time.time()
print(end-start)

if __name__ == "__main__":
    gvc = GVC()
    gvc.show_dashboard()
    sys.exit(gvc.App.exec_())
