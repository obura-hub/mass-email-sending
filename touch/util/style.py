stylesheet = """
QWidget{
    background : #FFF4F9;
}
QFrame#top_frame{
    border: 1px solid #999;
}
QFrame#container_frame{
    border: 1px solid #999;
}
QLineEdit{
    color: #636366;
    border-width: 1px;
    border-color: #76797C;
    border-style: solid;
    padding: 2px;
    border-radius: 5px;
    outline: none;
    margin : 0px;
    font-size: 14px;
    height : 30px;
    min-width: 250px;  
}

QLineEdit#sender_email{
    min-width: 250px;
    max-height: 20px;  
}

QLineEdit#last_scan{
    min-width: 100px;
    max-width: 100px;
    max-height: 20px;  
}

QPushButton{
    border-width: 1px;
    border-color: #76797C;
    border-style: solid;
    padding: 2px;
    border-radius: 5px;
    outline: none;
    margin : 0px;
    font-size: 14px;
}

QPushButton#refresh_button, QPushButton#upload_button{
    min-width: 60px;
    max-height: 20px;
    min-height: 20px;
    color: white;
}

QPushButton#upload_button{
    background-color: #5cb85c;
}
QPushButton#upload_button:hover{
    background-color: #4B8A08;
}
QPushButton#upload_button:disabled{
    background-color: #4B8A08;
}
QPushButton#refresh_button{
    background-color: #0275d8;
}
QPushButton#refresh_button:hover{
    background-color : #254F7B;
}
QPushButton#refresh_button:disabled{
    background-color: #254F7B;
}

QLabel#status{
    height : 20px;
    min-width: 150px;  
}

QLabel#status_queue_field, QLabel#status_sent_field{
    min-width: 20px;
    max-width: 20px;
}

QProgressBar{
    min-width: 300px;
    max-height: 20px;
}
"""