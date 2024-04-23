function validation(){
    if (document.regForm.username.value==""){
        document.getElementById('result').innerHTML='Enter Username*';
        return false;
    }
    else if (document.regForm.username.value.replace(/[^a-zA-Z]/g, "").length < 6){
        document.getElementById('result').innerHTML='Username at least 6 letters*';
        return false;
    }
    else if(document.regForm.username.value.length < 8){
        document.getElementById('result').innerHTML='Username must be at least 8-digits*'
        return false;
    }
    else if(document.regForm.email.value==''){
        document.getElementById('result').innerHTML='Enter your email*'
        return false;
    }
    else if(document.regForm.password.value==''){
        document.getElementById('result').innerHTML='Enter your password*'
        return false;
    }
    else if(document.regForm.password.value.length < 6){
        document.getElementById('result').innerHTML='Password must be 6-digits*'
        return false;
    }
    else if(document.regForm.repassword.value ==''){
        document.getElementById('result').innerHTML='Comfirm your password*'
        return false;
    }
    else if(document.regForm.repassword.value != document.regForm.password.value){
        document.getElementById('result').innerHTML='Password does not match*'
        return false; 
    }
    return true;
    }
