function inputValidation(inputTxt){
    
    var regx = /^[0-9a-zA-Z ]+$/;
    var textField = document.getElementById("textField");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 5){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = 'Good input';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'only numbers, letters And White space';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input is less than 5 chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

function fnameValidation(inputTxt){
    
    var regx = /^[a-zA-Z]+$/;
    var textField = document.getElementById("name");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 4){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = '**Only characters are allowed"';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = '**your firstname must include more chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = '**Please enter your firstname';
        textField.style.color = "red";
    }
}


function lnameValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s, ]+$/;
    var textField = document.getElementById("names");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 1){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'only characters allowded';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input mut me more than two chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

function addressValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s,()'-]*$/;
    var textField = document.getElementById("addr");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 5){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'only characters allowded';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input must me more chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}


function emailValidation(inputTxt){
    // ^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$
    var regx = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;
    var textField = document.getElementById("mail");
        
    if(inputTxt.value != '' ){
        if(inputTxt.value.match(regx)){
            textField.textContent = '';
            textField.style.color = "green";
        }else{
            textField.textContent = 'email is not valid!!!';
            textField.style.color = "red";
        }  
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

function phoneValidation(inputTxt){
    
    var regx = /^[6-9][0-9]{9}$/;
    var textField = document.getElementById("pho");
        
    if(inputTxt.value != '' ){
        if(inputTxt.value.match(regx)){
            textField.textContent = '';
            textField.style.color = "green";        
            }else{
                textField.textContent = '**not valid phone number';
                textField.style.color = "red";
            }  
    }else{
        textField.textContent = '**Please enter your phone number';
        textField.style.color = "red";
    }
}


function cityValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s, ]+$/;
    var textField = document.getElementById("cit");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 4){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = 'only characters allowded';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input mut me more than two chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = '**Please enter your city';
        textField.style.color = "red";
    }
}

function districtValidation(inputTxt){
    
    var regx = /^[a-zA-Z]+$/;
    var textField = document.getElementById("states");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 4){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'only characters allowded';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input mut me more than two chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}

function pincodeValidation(inputTxt){
    
    var regx = /^[6][0-9]{5}$/;
    var textField = document.getElementById("pin");
        
    if(inputTxt.value != '' ){
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = '**enter a valid pincode';
                textField.style.color = "red";
            }  
    }else{
        textField.textContent = '**Please enter the pincode';
        textField.style.color = "red";
    }
}


function passwordValidation(inputTxt){
    
    var regx = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}/;
    var textField = document.getElementById("pass1");
        
    if(inputTxt.value != '' ){
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'Must contain at least one number and one uppercase and lowercase letter';
                textField.style.color = "red";
            }    
    }else{
        textField.textContent = '**Password cannot be null!!';
        textField.style.color = "red";
    }
}


function cpasswordValidation(inputTxt){
    
    var regx =  document.getElementById("pwd").value;
    var regy =  document.getElementById("cpwd").value;
    var textField = document.getElementById("pass2");

        
    if(inputTxt.value != '' ){    
            if(regx == regy){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = '**passwords should be matching';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = '**confrim password cannot be null!!';
            textField.style.color = "red";
        }  
}
