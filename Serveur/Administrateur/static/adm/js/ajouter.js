document.getElementById('formulaire').addEventListener('submit',function(e){

    var erreur;
    var nom = document.getElementsByName('name');
    var email = document.getElementsByName('email');
    var mdp = document.getElementsByName('pass');

    if(!nom.values){
        erreur = "Veuillez renseigner le non d'utilisateur!"
    }
    if(!email.values){
        erreur = "Veuillez renseigner l'email!"
    }
    if(!mdp.values){
        erreur = "Veuillez renseigner le mot de passe!"
    }
    if (erreur){
        e.preventDefault();
        document.getElementById('mssg').innerHTML = erreur;
        return false;
    }else{
        alert("Utilisateur a été ajouter avec succés")
    }
})