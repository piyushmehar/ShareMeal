$(".nav-toggle").click(function () {
    $(".nav-menu").slideToggle();
  });

  $("#email").blur(function () {
    var emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var email = $(this).val();
    if (!emailRegex.test(email)) {
      alert("Invalid email format");
      return false;
    }
  });