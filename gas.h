/********************************************************************************
** Form generated from reading UI file 'gas.ui'
**
** Created by: Qt User Interface Compiler version 6.7.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef GAS_H
#define GAS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_gas
{
public:
    QWidget *centralwidget;
    QTabWidget *itemsGas;
    QWidget *prod;
    QWidget *formLayoutWidget;
    QFormLayout *formLayout;
    QLineEdit *rech;
    QLabel *label;
    QLabel *pllist;
    QTableWidget *stock;
    QPushButton *caisseAjoute;
    QScrollArea *scrollArea_2;
    QWidget *scrollAreaWidgetContents_2;
    QWidget *gridLayoutWidget_2;
    QGridLayout *itemsemb;
    QLabel *label_12;
    QWidget *admin;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QPushButton *modifier;
    QPushButton *supprime;
    QPushButton *ajoute;
    QPushButton *ajoutmasse;
    QPushButton *deleteall;
    QWidget *formLayoutWidget_2;
    QFormLayout *formLayout_2;
    QLabel *label_2;
    QLineEdit *rech2;
    QTableWidget *stockadm;
    QWidget *formLayoutWidget_4;
    QFormLayout *formLayout_4;
    QLabel *label_13;
    QLineEdit *quantitefiltre;
    QWidget *formLayoutWidget_5;
    QFormLayout *formLayout_5;
    QLabel *label_14;
    QLineEdit *reffiltre;
    QWidget *gridLayoutWidget_3;
    QGridLayout *gridLayout_2;
    QCheckBox *prixcroitfiltre;
    QLabel *label_15;
    QCheckBox *prixdecroitfiltre;
    QWidget *gridLayoutWidget_4;
    QGridLayout *gridLayout_3;
    QCheckBox *quantitecroit;
    QCheckBox *quantitedecroit;
    QLabel *label_16;
    QLabel *ti;
    QWidget *caisse;
    QListWidget *caisseache;
    QLabel *label_3;
    QTableWidget *receipt;
    QLineEdit *montant;
    QLabel *label_4;
    QPushButton *checkout;
    QLabel *label_5;
    QLabel *label_6;
    QPushButton *cancel_all;
    QPushButton *cancel_one;
    QLabel *label_9;
    QLabel *label_10;
    QWidget *recette;
    QWidget *formLayoutWidget_3;
    QFormLayout *formLayout_3;
    QLabel *label_7;
    QLabel *label_8;
    QLineEdit *rech_rec;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QListWidget *listrec;
    QListWidget *dataRec;
    QLabel *fdate;
    QLabel *label_11;
    QMenuBar *menubar;
    QMenu *menuHelp;
    QMenu *menuLicence;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *gas)
    {
        if (gas->objectName().isEmpty())
            gas->setObjectName("gas");
        gas->resize(1927, 1069);
        QFont font;
        font.setFamilies({QString::fromUtf8("NSimSun")});
        font.setPointSize(12);
        gas->setFont(font);
        QIcon icon;
        icon.addFile(QString::fromUtf8("../gas.ico"), QSize(), QIcon::Normal, QIcon::Off);
        gas->setWindowIcon(icon);
        gas->setToolButtonStyle(Qt::ToolButtonIconOnly);
        gas->setTabShape(QTabWidget::Triangular);
        centralwidget = new QWidget(gas);
        centralwidget->setObjectName("centralwidget");
        itemsGas = new QTabWidget(centralwidget);
        itemsGas->setObjectName("itemsGas");
        itemsGas->setGeometry(QRect(10, 0, 1921, 1051));
        QFont font1;
        font1.setPointSize(12);
        font1.setBold(true);
        itemsGas->setFont(font1);
        itemsGas->setAutoFillBackground(false);
        itemsGas->setStyleSheet(QString::fromUtf8(""));
        itemsGas->setInputMethodHints(Qt::ImhLowercaseOnly);
        itemsGas->setTabShape(QTabWidget::Triangular);
        itemsGas->setIconSize(QSize(32, 32));
        itemsGas->setElideMode(Qt::ElideNone);
        prod = new QWidget();
        prod->setObjectName("prod");
        formLayoutWidget = new QWidget(prod);
        formLayoutWidget->setObjectName("formLayoutWidget");
        formLayoutWidget->setGeometry(QRect(220, 40, 312, 71));
        formLayout = new QFormLayout(formLayoutWidget);
        formLayout->setObjectName("formLayout");
        formLayout->setHorizontalSpacing(10);
        formLayout->setVerticalSpacing(10);
        formLayout->setContentsMargins(0, 10, 0, 0);
        rech = new QLineEdit(formLayoutWidget);
        rech->setObjectName("rech");
        rech->setFont(font1);
        rech->setCursorPosition(0);

        formLayout->setWidget(0, QFormLayout::FieldRole, rech);

        label = new QLabel(formLayoutWidget);
        label->setObjectName("label");
        QFont font2;
        font2.setPointSize(14);
        font2.setBold(true);
        label->setFont(font2);

        formLayout->setWidget(0, QFormLayout::LabelRole, label);

        pllist = new QLabel(prod);
        pllist->setObjectName("pllist");
        pllist->setGeometry(QRect(10, 50, 241, 21));
        pllist->setFont(font1);
        stock = new QTableWidget(prod);
        if (stock->columnCount() < 5)
            stock->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        stock->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        stock->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        stock->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        stock->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        stock->setHorizontalHeaderItem(4, __qtablewidgetitem4);
        stock->setObjectName("stock");
        stock->setGeometry(QRect(20, 100, 1111, 531));
        stock->setStyleSheet(QString::fromUtf8(""));
        stock->setFrameShape(QFrame::NoFrame);
        stock->setFrameShadow(QFrame::Sunken);
        stock->setLineWidth(7);
        stock->setEditTriggers(QAbstractItemView::SelectedClicked);
        stock->setSelectionMode(QAbstractItemView::SingleSelection);
        stock->setSelectionBehavior(QAbstractItemView::SelectRows);
        stock->horizontalHeader()->setDefaultSectionSize(217);
        caisseAjoute = new QPushButton(prod);
        caisseAjoute->setObjectName("caisseAjoute");
        caisseAjoute->setGeometry(QRect(780, 40, 311, 51));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8("icons/add-to-cart.png"), QSize(), QIcon::Normal, QIcon::Off);
        caisseAjoute->setIcon(icon1);
        caisseAjoute->setIconSize(QSize(32, 32));
        caisseAjoute->setCheckable(false);
        scrollArea_2 = new QScrollArea(prod);
        scrollArea_2->setObjectName("scrollArea_2");
        scrollArea_2->setGeometry(QRect(1150, 120, 751, 851));
        scrollArea_2->setWidgetResizable(true);
        scrollAreaWidgetContents_2 = new QWidget();
        scrollAreaWidgetContents_2->setObjectName("scrollAreaWidgetContents_2");
        scrollAreaWidgetContents_2->setGeometry(QRect(0, 0, 749, 849));
        gridLayoutWidget_2 = new QWidget(scrollAreaWidgetContents_2);
        gridLayoutWidget_2->setObjectName("gridLayoutWidget_2");
        gridLayoutWidget_2->setGeometry(QRect(10, 10, 731, 831));
        itemsemb = new QGridLayout(gridLayoutWidget_2);
        itemsemb->setObjectName("itemsemb");
        itemsemb->setContentsMargins(0, 0, 0, 0);
        scrollArea_2->setWidget(scrollAreaWidgetContents_2);
        label_12 = new QLabel(prod);
        label_12->setObjectName("label_12");
        label_12->setGeometry(QRect(1170, 40, 161, 51));
        QIcon icon2;
        icon2.addFile(QString::fromUtf8("icons/shopping-cart.png"), QSize(), QIcon::Normal, QIcon::Off);
        itemsGas->addTab(prod, icon2, QString());
        admin = new QWidget();
        admin->setObjectName("admin");
        gridLayoutWidget = new QWidget(admin);
        gridLayoutWidget->setObjectName("gridLayoutWidget");
        gridLayoutWidget->setGeometry(QRect(10, 20, 1741, 171));
        gridLayout = new QGridLayout(gridLayoutWidget);
        gridLayout->setObjectName("gridLayout");
        gridLayout->setContentsMargins(0, 0, 0, 0);
        modifier = new QPushButton(gridLayoutWidget);
        modifier->setObjectName("modifier");
        QIcon icon3;
        icon3.addFile(QString::fromUtf8("icons/edit.png"), QSize(), QIcon::Normal, QIcon::Off);
        modifier->setIcon(icon3);
        modifier->setIconSize(QSize(32, 32));

        gridLayout->addWidget(modifier, 0, 1, 1, 1);

        supprime = new QPushButton(gridLayoutWidget);
        supprime->setObjectName("supprime");
        QIcon icon4;
        icon4.addFile(QString::fromUtf8("icons/delete.png"), QSize(), QIcon::Normal, QIcon::Off);
        supprime->setIcon(icon4);
        supprime->setIconSize(QSize(32, 32));

        gridLayout->addWidget(supprime, 0, 2, 1, 1);

        ajoute = new QPushButton(gridLayoutWidget);
        ajoute->setObjectName("ajoute");
        QIcon icon5;
        icon5.addFile(QString::fromUtf8("icons/add-product.png"), QSize(), QIcon::Normal, QIcon::Off);
        ajoute->setIcon(icon5);
        ajoute->setIconSize(QSize(32, 32));

        gridLayout->addWidget(ajoute, 0, 0, 1, 1);

        ajoutmasse = new QPushButton(gridLayoutWidget);
        ajoutmasse->setObjectName("ajoutmasse");
        QIcon icon6;
        icon6.addFile(QString::fromUtf8("icons/add.png"), QSize(), QIcon::Normal, QIcon::Off);
        ajoutmasse->setIcon(icon6);
        ajoutmasse->setIconSize(QSize(32, 32));

        gridLayout->addWidget(ajoutmasse, 0, 4, 1, 1);

        deleteall = new QPushButton(gridLayoutWidget);
        deleteall->setObjectName("deleteall");
        QIcon icon7;
        icon7.addFile(QString::fromUtf8("icons/icons8-delete-all-48.png"), QSize(), QIcon::Normal, QIcon::Off);
        deleteall->setIcon(icon7);
        deleteall->setIconSize(QSize(32, 32));

        gridLayout->addWidget(deleteall, 0, 3, 1, 1);

        formLayoutWidget_2 = new QWidget(admin);
        formLayoutWidget_2->setObjectName("formLayoutWidget_2");
        formLayoutWidget_2->setGeometry(QRect(10, 200, 421, 51));
        formLayout_2 = new QFormLayout(formLayoutWidget_2);
        formLayout_2->setObjectName("formLayout_2");
        formLayout_2->setHorizontalSpacing(10);
        formLayout_2->setVerticalSpacing(10);
        formLayout_2->setContentsMargins(0, 10, 0, 0);
        label_2 = new QLabel(formLayoutWidget_2);
        label_2->setObjectName("label_2");
        label_2->setFont(font2);

        formLayout_2->setWidget(0, QFormLayout::LabelRole, label_2);

        rech2 = new QLineEdit(formLayoutWidget_2);
        rech2->setObjectName("rech2");
        rech2->setFont(font1);

        formLayout_2->setWidget(0, QFormLayout::FieldRole, rech2);

        stockadm = new QTableWidget(admin);
        if (stockadm->columnCount() < 5)
            stockadm->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem5 = new QTableWidgetItem();
        stockadm->setHorizontalHeaderItem(0, __qtablewidgetitem5);
        QTableWidgetItem *__qtablewidgetitem6 = new QTableWidgetItem();
        stockadm->setHorizontalHeaderItem(1, __qtablewidgetitem6);
        QTableWidgetItem *__qtablewidgetitem7 = new QTableWidgetItem();
        stockadm->setHorizontalHeaderItem(2, __qtablewidgetitem7);
        QTableWidgetItem *__qtablewidgetitem8 = new QTableWidgetItem();
        stockadm->setHorizontalHeaderItem(3, __qtablewidgetitem8);
        QTableWidgetItem *__qtablewidgetitem9 = new QTableWidgetItem();
        stockadm->setHorizontalHeaderItem(4, __qtablewidgetitem9);
        stockadm->setObjectName("stockadm");
        stockadm->setGeometry(QRect(10, 260, 1091, 691));
        stockadm->setFrameShape(QFrame::NoFrame);
        stockadm->setFrameShadow(QFrame::Sunken);
        stockadm->setLineWidth(7);
        stockadm->setEditTriggers(QAbstractItemView::SelectedClicked);
        stockadm->setSelectionMode(QAbstractItemView::SingleSelection);
        stockadm->setSelectionBehavior(QAbstractItemView::SelectRows);
        stockadm->horizontalHeader()->setDefaultSectionSize(217);
        formLayoutWidget_4 = new QWidget(admin);
        formLayoutWidget_4->setObjectName("formLayoutWidget_4");
        formLayoutWidget_4->setGeometry(QRect(440, 210, 211, 41));
        formLayout_4 = new QFormLayout(formLayoutWidget_4);
        formLayout_4->setObjectName("formLayout_4");
        formLayout_4->setContentsMargins(0, 0, 0, 0);
        label_13 = new QLabel(formLayoutWidget_4);
        label_13->setObjectName("label_13");

        formLayout_4->setWidget(0, QFormLayout::LabelRole, label_13);

        quantitefiltre = new QLineEdit(formLayoutWidget_4);
        quantitefiltre->setObjectName("quantitefiltre");

        formLayout_4->setWidget(0, QFormLayout::FieldRole, quantitefiltre);

        formLayoutWidget_5 = new QWidget(admin);
        formLayoutWidget_5->setObjectName("formLayoutWidget_5");
        formLayoutWidget_5->setGeometry(QRect(650, 210, 206, 41));
        formLayout_5 = new QFormLayout(formLayoutWidget_5);
        formLayout_5->setObjectName("formLayout_5");
        formLayout_5->setContentsMargins(0, 0, 0, 0);
        label_14 = new QLabel(formLayoutWidget_5);
        label_14->setObjectName("label_14");

        formLayout_5->setWidget(0, QFormLayout::LabelRole, label_14);

        reffiltre = new QLineEdit(formLayoutWidget_5);
        reffiltre->setObjectName("reffiltre");

        formLayout_5->setWidget(0, QFormLayout::FieldRole, reffiltre);

        gridLayoutWidget_3 = new QWidget(admin);
        gridLayoutWidget_3->setObjectName("gridLayoutWidget_3");
        gridLayoutWidget_3->setGeometry(QRect(860, 200, 406, 58));
        gridLayout_2 = new QGridLayout(gridLayoutWidget_3);
        gridLayout_2->setObjectName("gridLayout_2");
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        prixcroitfiltre = new QCheckBox(gridLayoutWidget_3);
        prixcroitfiltre->setObjectName("prixcroitfiltre");

        gridLayout_2->addWidget(prixcroitfiltre, 1, 1, 1, 1);

        label_15 = new QLabel(gridLayoutWidget_3);
        label_15->setObjectName("label_15");

        gridLayout_2->addWidget(label_15, 1, 0, 1, 1);

        prixdecroitfiltre = new QCheckBox(gridLayoutWidget_3);
        prixdecroitfiltre->setObjectName("prixdecroitfiltre");

        gridLayout_2->addWidget(prixdecroitfiltre, 1, 2, 1, 1);

        gridLayoutWidget_4 = new QWidget(admin);
        gridLayoutWidget_4->setObjectName("gridLayoutWidget_4");
        gridLayoutWidget_4->setGeometry(QRect(1290, 200, 458, 61));
        gridLayout_3 = new QGridLayout(gridLayoutWidget_4);
        gridLayout_3->setObjectName("gridLayout_3");
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        quantitecroit = new QCheckBox(gridLayoutWidget_4);
        quantitecroit->setObjectName("quantitecroit");

        gridLayout_3->addWidget(quantitecroit, 1, 1, 1, 1);

        quantitedecroit = new QCheckBox(gridLayoutWidget_4);
        quantitedecroit->setObjectName("quantitedecroit");

        gridLayout_3->addWidget(quantitedecroit, 1, 2, 1, 1);

        label_16 = new QLabel(gridLayoutWidget_4);
        label_16->setObjectName("label_16");

        gridLayout_3->addWidget(label_16, 1, 0, 1, 1);

        ti = new QLabel(admin);
        ti->setObjectName("ti");
        ti->setGeometry(QRect(1140, 290, 511, 27));
        QIcon icon8;
        icon8.addFile(QString::fromUtf8("icons/loads.png"), QSize(), QIcon::Normal, QIcon::Off);
        itemsGas->addTab(admin, icon8, QString());
        caisse = new QWidget();
        caisse->setObjectName("caisse");
        caisseache = new QListWidget(caisse);
        caisseache->setObjectName("caisseache");
        caisseache->setGeometry(QRect(130, 130, 791, 381));
        caisseache->setEditTriggers(QAbstractItemView::SelectedClicked);
        caisseache->setSelectionBehavior(QAbstractItemView::SelectRows);
        label_3 = new QLabel(caisse);
        label_3->setObjectName("label_3");
        label_3->setGeometry(QRect(20, 70, 481, 41));
        receipt = new QTableWidget(caisse);
        if (receipt->rowCount() < 2)
            receipt->setRowCount(2);
        QTableWidgetItem *__qtablewidgetitem10 = new QTableWidgetItem();
        receipt->setVerticalHeaderItem(0, __qtablewidgetitem10);
        QTableWidgetItem *__qtablewidgetitem11 = new QTableWidgetItem();
        receipt->setVerticalHeaderItem(1, __qtablewidgetitem11);
        receipt->setObjectName("receipt");
        receipt->setGeometry(QRect(390, 530, 271, 81));
        montant = new QLineEdit(caisse);
        montant->setObjectName("montant");
        montant->setGeometry(QRect(950, 210, 151, 41));
        label_4 = new QLabel(caisse);
        label_4->setObjectName("label_4");
        label_4->setGeometry(QRect(950, 160, 171, 41));
        checkout = new QPushButton(caisse);
        checkout->setObjectName("checkout");
        checkout->setGeometry(QRect(950, 290, 151, 71));
        checkout->setStyleSheet(QString::fromUtf8(""));
        QIcon icon9;
        icon9.addFile(QString::fromUtf8("icons/bill.png"), QSize(), QIcon::Normal, QIcon::Off);
        checkout->setIcon(icon9);
        checkout->setIconSize(QSize(32, 32));
        label_5 = new QLabel(caisse);
        label_5->setObjectName("label_5");
        label_5->setGeometry(QRect(670, 540, 55, 21));
        label_6 = new QLabel(caisse);
        label_6->setObjectName("label_6");
        label_6->setGeometry(QRect(670, 570, 55, 21));
        cancel_all = new QPushButton(caisse);
        cancel_all->setObjectName("cancel_all");
        cancel_all->setGeometry(QRect(940, 370, 211, 71));
        QIcon icon10;
        icon10.addFile(QString::fromUtf8("icons/cancel-all.png"), QSize(), QIcon::Normal, QIcon::Off);
        cancel_all->setIcon(icon10);
        cancel_all->setIconSize(QSize(32, 32));
        cancel_one = new QPushButton(caisse);
        cancel_one->setObjectName("cancel_one");
        cancel_one->setGeometry(QRect(940, 460, 211, 71));
        QIcon icon11;
        icon11.addFile(QString::fromUtf8("icons/cancel.png"), QSize(), QIcon::Normal, QIcon::Off);
        cancel_one->setIcon(icon11);
        cancel_one->setIconSize(QSize(32, 32));
        label_9 = new QLabel(caisse);
        label_9->setObjectName("label_9");
        label_9->setGeometry(QRect(320, 530, 161, 61));
        label_9->setPixmap(QPixmap(QString::fromUtf8("icons/icons8-money-64.png")));
        label_10 = new QLabel(caisse);
        label_10->setObjectName("label_10");
        label_10->setGeometry(QRect(1110, 200, 91, 61));
        label_10->setPixmap(QPixmap(QString::fromUtf8("icons/icons8-dolar-64.png")));
        QIcon icon12;
        icon12.addFile(QString::fromUtf8("icons/cash-register.png"), QSize(), QIcon::Normal, QIcon::Off);
        itemsGas->addTab(caisse, icon12, QString());
        recette = new QWidget();
        recette->setObjectName("recette");
        formLayoutWidget_3 = new QWidget(recette);
        formLayoutWidget_3->setObjectName("formLayoutWidget_3");
        formLayoutWidget_3->setGeometry(QRect(100, 30, 401, 91));
        formLayout_3 = new QFormLayout(formLayoutWidget_3);
        formLayout_3->setObjectName("formLayout_3");
        formLayout_3->setHorizontalSpacing(10);
        formLayout_3->setVerticalSpacing(10);
        formLayout_3->setContentsMargins(0, 10, 0, 0);
        label_7 = new QLabel(formLayoutWidget_3);
        label_7->setObjectName("label_7");
        label_7->setFont(font2);

        formLayout_3->setWidget(1, QFormLayout::LabelRole, label_7);

        label_8 = new QLabel(formLayoutWidget_3);
        label_8->setObjectName("label_8");

        formLayout_3->setWidget(0, QFormLayout::LabelRole, label_8);

        rech_rec = new QLineEdit(formLayoutWidget_3);
        rech_rec->setObjectName("rech_rec");
        rech_rec->setFont(font1);

        formLayout_3->setWidget(0, QFormLayout::FieldRole, rech_rec);

        scrollArea = new QScrollArea(recette);
        scrollArea->setObjectName("scrollArea");
        scrollArea->setGeometry(QRect(40, 100, 461, 521));
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName("scrollAreaWidgetContents");
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 459, 519));
        listrec = new QListWidget(scrollAreaWidgetContents);
        listrec->setObjectName("listrec");
        listrec->setGeometry(QRect(0, 0, 461, 521));
        listrec->setAutoScrollMargin(30);
        listrec->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
        listrec->setHorizontalScrollMode(QAbstractItemView::ScrollPerPixel);
        listrec->setMovement(QListView::Free);
        listrec->setResizeMode(QListView::Adjust);
        scrollArea->setWidget(scrollAreaWidgetContents);
        dataRec = new QListWidget(recette);
        dataRec->setObjectName("dataRec");
        dataRec->setEnabled(false);
        dataRec->setGeometry(QRect(590, 160, 651, 71));
        dataRec->setAutoScrollMargin(30);
        fdate = new QLabel(recette);
        fdate->setObjectName("fdate");
        fdate->setGeometry(QRect(720, 20, 411, 31));
        label_11 = new QLabel(recette);
        label_11->setObjectName("label_11");
        label_11->setGeometry(QRect(530, 170, 51, 61));
        label_11->setPixmap(QPixmap(QString::fromUtf8("icons/icons8-total-sales-50.png")));
        itemsGas->addTab(recette, icon2, QString());
        gas->setCentralWidget(centralwidget);
        menubar = new QMenuBar(gas);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 1927, 26));
        menuHelp = new QMenu(menubar);
        menuHelp->setObjectName("menuHelp");
        menuLicence = new QMenu(menubar);
        menuLicence->setObjectName("menuLicence");
        gas->setMenuBar(menubar);
        statusbar = new QStatusBar(gas);
        statusbar->setObjectName("statusbar");
        gas->setStatusBar(statusbar);

        menubar->addAction(menuHelp->menuAction());
        menubar->addAction(menuLicence->menuAction());
        menuLicence->addSeparator();

        retranslateUi(gas);

        itemsGas->setCurrentIndex(2);


        QMetaObject::connectSlotsByName(gas);
    } // setupUi

    void retranslateUi(QMainWindow *gas)
    {
        gas->setWindowTitle(QCoreApplication::translate("gas", "Gestion des Ventes Commerical", nullptr));
        label->setText(QCoreApplication::translate("gas", "Recherche", nullptr));
        pllist->setText(QCoreApplication::translate("gas", "List des Produits", nullptr));
        QTableWidgetItem *___qtablewidgetitem = stock->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QCoreApplication::translate("gas", "Nom", nullptr));
        QTableWidgetItem *___qtablewidgetitem1 = stock->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QCoreApplication::translate("gas", "Description", nullptr));
        QTableWidgetItem *___qtablewidgetitem2 = stock->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QCoreApplication::translate("gas", "Prix Unitaire", nullptr));
        QTableWidgetItem *___qtablewidgetitem3 = stock->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QCoreApplication::translate("gas", "Quantit\303\251", nullptr));
        QTableWidgetItem *___qtablewidgetitem4 = stock->horizontalHeaderItem(4);
        ___qtablewidgetitem4->setText(QCoreApplication::translate("gas", "Reference", nullptr));
        caisseAjoute->setText(QCoreApplication::translate("gas", "Ajouter a la caisse", nullptr));
        label_12->setText(QCoreApplication::translate("gas", "Ajout Rapide", nullptr));
        itemsGas->setTabText(itemsGas->indexOf(prod), QCoreApplication::translate("gas", "Panier", nullptr));
        modifier->setText(QCoreApplication::translate("gas", "Modifier un produit", nullptr));
        supprime->setText(QCoreApplication::translate("gas", "Supprimer un produit", nullptr));
        ajoute->setText(QCoreApplication::translate("gas", "Ajouter un produit", nullptr));
        ajoutmasse->setText(QCoreApplication::translate("gas", "Ajouter des produits avec un fichier .csv", nullptr));
        deleteall->setText(QCoreApplication::translate("gas", "Supprimer tous les produits", nullptr));
        label_2->setText(QCoreApplication::translate("gas", "Recherche", nullptr));
        QTableWidgetItem *___qtablewidgetitem5 = stockadm->horizontalHeaderItem(0);
        ___qtablewidgetitem5->setText(QCoreApplication::translate("gas", "Nom", nullptr));
        QTableWidgetItem *___qtablewidgetitem6 = stockadm->horizontalHeaderItem(1);
        ___qtablewidgetitem6->setText(QCoreApplication::translate("gas", "Description", nullptr));
        QTableWidgetItem *___qtablewidgetitem7 = stockadm->horizontalHeaderItem(2);
        ___qtablewidgetitem7->setText(QCoreApplication::translate("gas", "Prix Unitaire", nullptr));
        QTableWidgetItem *___qtablewidgetitem8 = stockadm->horizontalHeaderItem(3);
        ___qtablewidgetitem8->setText(QCoreApplication::translate("gas", "Quantit\303\251", nullptr));
        QTableWidgetItem *___qtablewidgetitem9 = stockadm->horizontalHeaderItem(4);
        ___qtablewidgetitem9->setText(QCoreApplication::translate("gas", "Reference", nullptr));
        label_13->setText(QCoreApplication::translate("gas", "Quantit\303\251 >=", nullptr));
        label_14->setText(QCoreApplication::translate("gas", "Reference", nullptr));
        prixcroitfiltre->setText(QCoreApplication::translate("gas", "Croissant", nullptr));
        label_15->setText(QCoreApplication::translate("gas", "Prix", nullptr));
        prixdecroitfiltre->setText(QCoreApplication::translate("gas", "Decroissant", nullptr));
        quantitecroit->setText(QCoreApplication::translate("gas", "Croissant", nullptr));
        quantitedecroit->setText(QCoreApplication::translate("gas", "Decroissant", nullptr));
        label_16->setText(QCoreApplication::translate("gas", "Quantit\303\251", nullptr));
        ti->setText(QCoreApplication::translate("gas", ".", nullptr));
        itemsGas->setTabText(itemsGas->indexOf(admin), QCoreApplication::translate("gas", "Stock", nullptr));
        label_3->setText(QCoreApplication::translate("gas", "Liste des produits dans ligne vente", nullptr));
        QTableWidgetItem *___qtablewidgetitem10 = receipt->verticalHeaderItem(0);
        ___qtablewidgetitem10->setText(QCoreApplication::translate("gas", "Total", nullptr));
        QTableWidgetItem *___qtablewidgetitem11 = receipt->verticalHeaderItem(1);
        ___qtablewidgetitem11->setText(QCoreApplication::translate("gas", "Rendu", nullptr));
        label_4->setText(QCoreApplication::translate("gas", "Montant(CASH)", nullptr));
        checkout->setText(QCoreApplication::translate("gas", "Caisse", nullptr));
        label_5->setText(QCoreApplication::translate("gas", "DT", nullptr));
        label_6->setText(QCoreApplication::translate("gas", "DT", nullptr));
        cancel_all->setText(QCoreApplication::translate("gas", "Annuler tous", nullptr));
        cancel_one->setText(QCoreApplication::translate("gas", "Annuler une", nullptr));
        label_9->setText(QString());
        label_10->setText(QString());
        itemsGas->setTabText(itemsGas->indexOf(caisse), QCoreApplication::translate("gas", "Caisse", nullptr));
        label_7->setText(QString());
        label_8->setText(QCoreApplication::translate("gas", "Recherche", nullptr));
        fdate->setText(QCoreApplication::translate("gas", ".", nullptr));
        label_11->setText(QString());
        itemsGas->setTabText(itemsGas->indexOf(recette), QCoreApplication::translate("gas", "Recettes", nullptr));
        menuHelp->setTitle(QCoreApplication::translate("gas", "A propos", nullptr));
        menuLicence->setTitle(QCoreApplication::translate("gas", "Licence", nullptr));
    } // retranslateUi

};

namespace Ui {
    class gas: public Ui_gas {};
} // namespace Ui

QT_END_NAMESPACE

#endif // GAS_H
