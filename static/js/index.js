var dd = false;

function dropDown() {
    if (dd === false) {
        $(".fa-bars").css({
            transform: 'rotate(90deg)',
            transition: '0.5s ease-in-out'
        });
        $(".menu").css({
            display: 'block',
            transform: 'translateY(0)',
            transition: '1s ease-in-out',
        });
        dd = true;
    } else {
        $(".fa-bars").css("transform", "rotate(0deg)");
        $(".menu").css("display", "none");
        dd = false;
    }

}


//Gallery

var arr = [];
for (var i = 0; i < $(".gallery img").length; i++) {
    arr[i] = $(".gallery img")[i];
}


$(".gallery img").click(function (e) {
    $("body").append('<div class="overlay"><img src="" number=""><div class="controls"> <div class="ctrl left" onclick="Prev()"></div><div class="ctrl close" onclick="Close()"></div><div class="ctrl right" onclick="Next()"></div></div></div>');
    Change($(e.target).attr("number"))
});

function Prev() {
    num = parseInt($(".overlay img").attr("number"), 10)
    if (num === 0) {
        Change(arr.length - 1)
    } else {
        Change(num - 1)
    }
}

function Next() {
    num = parseInt($(".overlay img").attr("number"), 10)
    if (num === arr.length - 1) {
        Change(0)
    } else {
        Change(num + 1)
    }
}

function Close() {
    $(".overlay").remove()
}

function Change(id) {
    adress = $(arr[id]).attr("src")
    $(".overlay img").attr("src", adress).attr("number", id)
}

$('html').keydown(function (e) {
    if(e.which === 37){
        Prev();
    }
    if(e.which === 39){
        Next();
    }
    if(e.which === 13 || e.which === 27){
        Close();
    }
});