from django.shortcuts import render
from django.http import HttpResponse


def index(request):


    output = """ <!doctype html>
<html lang="en" class="no-js">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="https://fonts.googleapis.com/css?family=Lato:400,700" rel="stylesheet">
	<link rel="stylesheet" href="css/reset.css"> <!-- CSS reset -->
	<link rel="stylesheet" href="css/style.css"> <!-- Resource style -->
  	
	<title>Product Builder | CodyHouse</title>
</head>
<body>
<div class="cd-product-builder">
	<header class="main-header">
		<h1>Product Builder</h1>
		
		<nav class="cd-builder-main-nav disabled">
			<ul>
				<li class="active"><a href="#models">Models</a></li>
				<li><a href="#colors">Colors</a></li>
				<li><a href="#accessories">Accessories</a></li>
				<li><a href="#summary">Summary</a></li>
			</ul>
		</nav>

		<a href="https://codyhouse.co/?p=16220" class="cd-nugget-info hide-on-mobile">Article &amp; Download</a>
	</header>

	<div class="cd-builder-steps">
		<ul>
			<li data-selection="models" class="active builder-step">
				<section class="cd-step-content">
					<header>
						<h1>Select Model</h1>
						<span class="steps-indicator">Step <b>1</b> of 4</span>
					</header>

					<a href="https://codyhouse.co/?p=16220" class="cd-nugget-info hide-on-desktop">Article &amp; Download</a>

					<ul class="models-list options-list cd-col-2">
						<li class="js-option js-radio" data-price="42400" data-model="product-01">
							<span class="name">BMW i3</span>
							<img src="img/product01_col01.jpg" alt="BMW i3">
							<span class="price">from $42.400</span>
							<div class="radio"></div>
						</li>

						<li class="js-option js-radio" data-price="140700" data-model="product-02">
							<span class="name">BMW i8</span>
							<img src="img/product02_col01.jpg" alt="BMW i8">
							<span class="price">from $140.700</span>
							<div class="radio"></div>
						</li>
					</ul>
				</section>
			</li>
			<!-- additional content will be inserted using ajax -->
		</ul>
	</div>

	<footer class="cd-builder-footer disabled step-1">
		<div class="selected-product">
			<img src="img/product01_col01.jpg" alt="Product preview">

			<div class="tot-price">
				<span>Total</span>
				<span class="total">$<b>0</b></span>
			</div>
		</div>
		
		<nav class="cd-builder-secondary-nav">
			<ul>
				<li class="next nav-item">
					<ul>
						<li class="visible"><a href="#0">Colors</a></li>
						<li><a href="#0">Accessories</a></li>
						<li><a href="#0">Summary</a></li>
						<li class="buy"><a href="#0">Buy Now</a></li>
					</ul>
				</li>
				<li class="prev nav-item">
					<ul>
						<li class="visible"><a href="#0">Models</a></li>
						<li><a href="#0">Models</a></li>
						<li><a href="#0">Colors</a></li>
						<li><a href="#0">Accessories</a></li>
					</ul>
				</li>
			</ul>
		</nav>

		<span class="alert">Please, select a model first!</span>
	</footer>
</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js"></script>
<script>
	if( !window.jQuery ) document.write('<script src="js/jquery-3.0.0.min.js"><\/script>');
</script>
<script src="js/main.js"></script> <!-- Resource jQuery -->
</body>
</html>"""





    
    return HttpResponse(output)





