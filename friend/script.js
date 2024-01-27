import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-app.js";
import { getFirestore, collection, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-firestore.js";
import { getStorage, ref as storageRef, uploadBytes } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyC0hbLRJ3KpsY8k9APSOSRKVhS7J42jVuU",
  authDomain: "netwark-10966.firebaseapp.com",
  projectId: "netwark-10966",
  storageBucket: "netwark-10966.appspot.com",
  messagingSenderId: "362620757034",
  appId: "1:362620757034:web:96b1535ccdf3b1431f0f53",
  measurementId: "G-8KWZWSXTFY"
};

const app = initializeApp(firebaseConfig);


// data

const db = getFirestore(app);

// storage

const storage = getStorage(app, "gs://netwark-10966.appspot.com");



// helper methods

const getElementVal = (id) => {
  return document.getElementById(id).value;
}

function getCheckedInterests() {
  const checkboxes = document.querySelectorAll('.interestsContainer input[type="checkbox"]:checked');
  const interests = [];

  checkboxes.forEach((checkbox) => {
    const label = document.querySelector(`label[for="${checkbox.id}"]`);
    interests.push(label.textContent);
  });

  return interests;
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}


// submit

document.getElementById('submit').addEventListener('click', submitForm);

async function submitForm(e) {
  e.preventDefault();


  const fname = capitalizeFirstLetter(getElementVal('fname'));
  const lname = capitalizeFirstLetter(getElementVal('lname'));
  const hometown = capitalizeFirstLetter(getElementVal('hometown'));
  const role = capitalizeFirstLetter(getElementVal('role'));
  const position = capitalizeFirstLetter(getElementVal('position'));
  const organization = capitalizeFirstLetter(getElementVal('organization'));
  const interests = getCheckedInterests();
  const linkedin = getElementVal('linkedin');
  const image = document.getElementById('pic').files[0];

  const userID = fname + '_' + lname;

  const data = {
    first_name: fname,
    last_name: lname,
    hometown: hometown,
    team_role: role,
    position: position,
    interests: interests,
    organization: organization,
    contact: linkedin,
  };

  // storage
  const userImagesRef = storageRef(storage, 'user_images/' + userID);
  await uploadBytes(userImagesRef, image);

  // data
  const collectionRef = collection(db, 'users');
  const docRef = doc(collectionRef, userID);
  await setDoc(docRef, data);

  // clear form
  document.getElementById('form').reset();
}