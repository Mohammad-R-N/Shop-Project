(function ($) {
    'use strict';

	// scroll to top js
	var scroll = $(".go-top");
	scroll.on('click', function() {
		$('html , body').animate({
			scrollTop: 0
		}, 300);
	});


	// active mobile-menu
	jQuery('#mobile-menu').meanmenu({
		meanScreenWidth: '991',
		meanMenuContainer: '.mobile-menu'
	});

	// toggle search bar
	$('.search .search__trigger .open').click(function () {
		$(".search .search__trigger .open").hide();
		$(".search .search__trigger .close").show();
		$('.search__form').addClass('active');
	});
	$('.search .search__trigger .close').click(function () {
		$(".search .search__trigger .open").show();
		$(".search .search__trigger .close").hide();
		$('.search__form').removeClass('active');
	});

	// Side menu info
	$(".hamburger-trigger").on("click", function (e) {
		e.preventDefault();
		$(".side-info-wrapper").toggleClass("show");
		$("body").addClass("on-side");
		$('.overlay').addClass('active');
		$(this).addClass('active');
	});

	$(".side-info__close > a").on("click", function (e) {
		e.preventDefault();
		$(".side-info-wrapper").removeClass("show");
		$("body").removeClass("on-side");
		$('.overlay').removeClass('active');
		$('.hamburger-trigger').removeClass('active');
	});

	$('.overlay').on('click', function () {
		$(this).removeClass('active');
		$(".side-info-wrapper").removeClass("show");
		$("body").removeClass("on-side");
		$('.hamburger-trigger').removeClass('active');
	});

	// cart info
	$(".cart-trigger").on("click", function (e) {
		e.preventDefault();
		$(".cart-bar-wrapper").toggleClass("show");
		$("body").addClass("on-side");
		$('.overlay').addClass('active');
		$(this).addClass('active');
	});

	$(".cart-bar__close > a").on("click", function (e) {
		e.preventDefault();
		$(".cart-bar-wrapper").removeClass("show");
		$("body").removeClass("on-side");
		$('.overlay').removeClass('active');
		$('.cart-trigger').removeClass('active');
	});

	$('.overlay').on('click', function () {
		$(this).removeClass('active');
		$(".cart-bar-wrapper").removeClass("show");
		$("body").removeClass("on-side");
		$('.cart-trigger').removeClass('active');
	});

	
	//  product popup
	$('.view').on('click',function() {
		$('.overlay, .product-popup-1').addClass('show-popup');
	});

	$('.product-highlight__trigger').on('click',function() {
		$('.overlay, .popup-coffe-mechine').addClass('show-popup');
	});

	$('.overlay,.product-p-close').on('click',function() {
		$('.overlay, .popup-coffe-mechine, .product-popup').removeClass('show-popup');
	});

	// Activate lightcase
	$('a[data-rel^=lightcase]').lightcase();


	//for menu active class
	$('.popular-menu__filter button').on('click', function (event) {
		$(this).siblings('.active').removeClass('active');
		$(this).addClass('active');
		event.preventDefault();
	});

	$('.pp__item').on('mouseenter', function () {
		$(this).addClass('active').parent().siblings().find('.pp__item').removeClass('active');
	});


	
})(jQuery);

    function updatePriceDisplay(counterScoreId) {
        var counterScore = document.getElementById(counterScoreId);
        var quantity = parseInt(counterScore.innerText);
        var priceElement = document.querySelector("#" + counterScoreId).closest(".card__wrapper").querySelector(".card__price");
        var pricePerItem = parseFloat(priceElement.dataset.price);
        var totalPrice = pricePerItem * quantity;
        var itemPriceElement = document.getElementById(priceElement.id);
        itemPriceElement.innerText = '$ ' + totalPrice.toFixed(2);
    }

    // Function to increment the counter
    function incrementCounter(counterScoreId) {
        var counterScore = document.getElementById(counterScoreId);
        var currentScore = parseInt(counterScore.innerText);
        counterScore.innerText = currentScore + 1;
        updatePriceDisplay(counterScoreId);
    }

    // Function to decrement the counter
    function decrementCounter(counterScoreId) {
        var counterScore = document.getElementById(counterScoreId);
        var currentScore = parseInt(counterScore.innerText);
        if (currentScore > 1) {
            counterScore.innerText = currentScore - 1;
            updatePriceDisplay(counterScoreId);
        }
    }

    // Initial price display update
    updatePriceDisplay('counterScore1');
    updatePriceDisplay('counterScore2');
    updatePriceDisplay('counterScore3');



