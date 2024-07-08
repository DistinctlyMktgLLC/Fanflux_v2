import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCQ_Jcq1eCyylUpXi0lDO3WC70mOAWDoao",
    "authDomain": "fanflux-299ad.firebaseapp.com",
    "databaseURL": "https://console.firebase.google.com/u/0/project/fanflux-299ad/database/fanflux-299ad-default-rtdb/data/~2F",
    "projectId": "fanflux-299ad",
    "storageBucket": "fanflux-299ad.appspot.com",
    "messagingSenderId": "643979891706",
    "appId": "1:643979891706:web:107a98abb3372ec3774a43",
    "measurementId": "G-CJ1KQVDMR2"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
