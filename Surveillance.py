#Created by Megabus, you can re-use all of this code freely

import cv2
import numpy
import datetime
import shutil

##Email BASE
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'A GMAIL Account with less secure apps enabled'
email_password = ' '
email_send = ' '
##Fin Email BASE


capture = cv2.VideoCapture(0)

FondInitial = cv2.createBackgroundSubtractorMOG2(50, 200, True) # Historique, Seuil, DetectionOmbres 

CompteurFrame = 0

CompteurIntrusion = 0



while(1):

    
    date = str(datetime.datetime.now())
    intrusion = 'Intrusion en cours ' + date

    dateInt = datetime.datetime.now()
    #exportIntrusion = 'Intrusion le '+ str(dateInt.hour) +'-'+ str(dateInt.minute)+'-'+ str(dateInt.second)
    #exportIntrusion = 'Intrusion le '+ str(dateInt.day)+'-'+ str(dateInt.month) + ' à ' + str(dateInt.hour) +'-'+ str(dateInt.minute)
    exportIntrusion = 'photosExport'


    ret, frame = capture.read()

    if not ret:
        break
        #Si le compteur n'est pas lancé l'algorithme se ferme

    CompteurFrame += 1
    #Implanter un compteur est nécessaire pour qu'OpenCV distingue les images qu'il compare

    #Le Premier plan se superpose au flux vidéo pour analyser les différences
    MasquePremierPlan = FondInitial.apply(frame)

    CompteurPixel = numpy.count_nonzero(MasquePremierPlan) #Compte les pixels qui change selon les frames

    print('Frame N°: %d, Variation: %d' % (CompteurFrame, CompteurPixel))
    print(exportIntrusion)

    if (CompteurFrame > 1 and CompteurPixel > 3000):
    #La variable CompteurPixel définira le seuil de détection de mouvement
        print('Intrusion en cours')
        cv2.putText(frame, intrusion , (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (66, 125, 244), 2, cv2.LINE_AA)
        CompteurIntrusion += 1

        NumeroCompteurIntrusion = str(CompteurIntrusion)
        PhotoCompteurIntrusion = str('Export/'+NumeroCompteurIntrusion + '.jpg')

        cv2.imwrite(PhotoCompteurIntrusion,frame)
        if (CompteurIntrusion == 50):
            shutil.make_archive(exportIntrusion, 'zip', 'Export')
            CompteurIntrusion=0

            #Envoi Email
            subject = 'Intrusion Détectée dans votre salon'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject

            body = 'Les photos prisent par votre Raspberry sont joint à ce mail'
            msg.attach(MIMEText(body,'plain'))

            filename= str(exportIntrusion+'.zip')
            attachment  =open(filename,'rb')

            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email_user,email_password)


            server.sendmail(email_user,email_send,text)
            server.quit()
            ##Fin E-Mail

    cv2.imshow('Video', frame)
    cv2.imshow('Masque de Detection', MasquePremierPlan)

    if CompteurFrame == 1000:
        CompteurFrame = 0

    k = cv2.waitKey(1) #Echap (Touche 27) casse la boucle donc, quitte le programme
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()


    






