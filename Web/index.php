<?php
				$db = mysqli_connect("193.93.253.25","codespo","45Pvilfd","codespo_metinstitutt") or die('FEILMELDING: Klarte ikke å koble til databasen');

        $query = "SELECT * FROM data_main_min ORDER BY ID DESC LIMIT 1";
        mysqli_query($db, $query) or die('FEILMELDING: Feil i inntasting');

        $result = mysqli_query($db, $query);

        
        while ($row = mysqli_fetch_array($result)) {
         $nowtime = $row["TIMESTAMP"];
         $nowtemp = $row["CELSIUS"];
        }
        mysqli_close($db);

				$db2 = mysqli_connect("193.93.253.25","codespo","45Pvilfd","codespo_metinstitutt") or die('FEILMELDING: Klarte ikke å koble til databasen');

				$query2 = "SELECT * FROM data_main_min ORDER BY ID DESC";
        mysqli_query($db2, $query2) or die('FEILMELDING: Feil i inntasting');

        $result2 = mysqli_query($db2, $query2);

        
        while ($row2 = mysqli_fetch_array($result2)) {
         $uptimeData += 1;
        }

				$past = strtotime('2017-12-12');
				$now  = (new DateTime())->getTimestamp();
				$passedTime = (($now - $past)/60);
				
				$uptimeVar = ($uptimeData - 12703);

				$uptime = (($uptimeVar) / ($passedTime) * 100);

        mysqli_close($db2);

?>

<html>
  <head>
    <title>Meteorologisk Institutt</title>
    <!-- Libraries -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
		<link rel="icon" href="https://i1.wp.com/medtechboston.medstro.com/wp-content/uploads/2015/09/MedTech-M-Only-Logo-No-Border-400x400.png">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/remodal/1.1.1/remodal.js"></script>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remodal/1.1.1/remodal.css" />
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remodal/1.1.1/remodal-default-theme.css" />
		<script src="../met/Chart.js"></script>
		
    <style>
      body {
        margin: 0;
        padding; 0;
        
        font-family: Montserrat,"Helvetica Neue",Helvetica,Arial,sans-serif;
      }
			
			li {
				list-style: none;
			}
      
      .page--front {
        background-image: url("resources/img/graph.png");
        background-position: center;
        background-size: cover;
        height: 100vh;
      }
      
      .page--front .header {
        position: fixed;
        width: 90vw;
        z-index: 99;
        padding: 2% 5% 2% 5%;
				background-color: transparent;
      }
      
      .page--front .header h1 {
        color: rgba(255, 255, 255, 1);
        text-transform: uppercase;
        font-weight: 200;
        font-size: 18px;
        
        display: inline-block;
      }
      
      .page--front .header .fa {
        color: white;
      }
      
      .page--front .header .header--right {
        float: right;
      }
      
      .page--front .header .header--right ul {
        list-style: none;
        float: right;
      }
      
      .page--front .header .header--right li {
        display: inline-block;
        
        font-size: 18px;
        font-weight: 400;
        color: white;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-right: 40px;
      }
      
      .page--front .bigtext {
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
      }
      
      .page--front .bigtext h2 {
        color: white;
        text-transform: uppercase;
        font-size: 50px;
        text-align: center;
      }
      
      .scrollcircle {
				width: 100%;
				position: absolute;
				bottom: 10%;
				text-align: center;
			}
      
      .page--ouroffer {
        height: auto;
      }
			
			.container {
        width: 46%;
        height: 47.9%;
        display: inline-block;
				margin: 2%;
        justify-content: space-between;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
      }
      
      .left {
        background-image: url("resources/img/graph2.png");
      }
      
      .right {
        background-image: url("resources/img/cables.png");
      }
			
			.page--apply {
        height: auto;
      }
			
			.page--apply .socials {
				background: url("resources/img/notes.png");
				background-size: cover;
				background-position: bottom;
				margin: 2%;
				padding: 0.5%;
				height: auto;
			}
			
			.page--apply .uptime {
				background: url("resources/img/clock.jpg");
				background-size: cover;
				background-position: top;
				color: white;
				margin: 2%;
				padding: 0.5%;
				height: auto;
			}
			
			.page--apply .socials h1 {
				font-size: 40px;
				color: white;
				text-transform: uppercase;
			}
			
			.page--apply .socials p {
				font-size: 30px;
				color: white;
				text-transform: uppercase;
			}
      
      #img--text {
        position: absolute; 
        top: 100px;
        color: white;
        background-color: rgba(255, 255, 255, 0.4);
        padding: 2% 10% 2% 10%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
      }
      
      @keyframes headerFadeIn {
        0% {padding: 2% 5% 2% 5%; background-color: transparent;}
        100% {padding: 0.5% 5% 0.5% 5%; background-color: rgba(0, 0, 0, 0.8);}
      }
      
      @keyframes headerFadeOut {
        0% {padding: 1% 5% 1% 5%; background-color: rgba(0, 0, 0, 0.8);}
        100% {padding: 2% 5% 2% 5%; background-color: transparent;}
      }
      
      
      @media only screen and (max-width: 993px) {
				
				.page--front .header h1 {
					font-size: 2em;
				}
				
				.page--front .header .header--right li {
					font-size: 2em;
					padding: 5px;
				}
        
        .page--front .bigtext h2 {
          font-size: 100px;
          width: 100vw;
        }
				
				.scrollcircle {
					font-size: 2em;
				}
				
				.page--ouroffer .header h1 {
					font-size: 80px;
				}
				
				.page--ouroffer .offer--listone {
					padding: 1% 2% 1% 2%;
					margin: 2% 0% 5% 0%;
					width: 70%;
					display: block;
				}
        
        #img--text {
          position: absolute; 
          top: 100px;
          color: white;
          background-color: rgba(255, 255, 255, 0.4);
          padding: 2% 10% 2% 10%;
          font-size: 70px;
          left: 50%;
          transform: translateX(-50%) translateY(-50%);
        }
        
        .page--apply .socials h1 {
          font-size: 70px;
          color: white;
          text-transform: uppercase;
        }

        .page--apply .socials p {
          font-size: 40px;
          color: white;
          text-transform: uppercase;
        }
				
				.container {
					width: 96%;
					height: 47.9%;
					display: inline-block;
					margin: 2%;
					justify-content: space-between;
					background-size: cover;
					background-repeat: no-repeat;
					background-position: center;
				}
				
				.page--apply .header h1 {
					font-size: 80px;
				}
				
				.page--apply .header h2 {
					font-size: 60px;
				}
				
				.page--apply .header p {
					font-size: 40px;
					padding: 4%;
				}
        	
      }
    </style>
    <script>
      $(document).ready(function(){
        $("#scrollbtn").click(function() {
              $('html, body').animate({
                  scrollTop: -100 + $(".page--ouroffer").offset().top
              }, 1000);
          });
        
        $("#scroll--ouroffer").click(function() {
              $('html, body').animate({
                  scrollTop: -100 + $(".page--ouroffer").offset().top
              }, 1000);
          });
				
				$("#scroll--apply").click(function() {
              $('html, body').animate({
                  scrollTop: -100 + $(".page--apply").offset().top
              }, 1000);
          });
        
        
        
        $(window).scroll(function() {
          var height = $(window).scrollTop();

          if(height  > 25) {
            document.getElementsByClassName("header")[0].style.animation = "headerFadeIn 0.5s forwards";
          } else {
            document.getElementsByClassName("header")[0].style.animation = "headerFadeOut 0.5s forwards";
          }
        });
        
      });
    </script>
	
  </head>
  <body  onload="ajaxCall(); ajaxCall_24h(); ajaxCall_allTime();">
    <div class="page--front">
      <div class="header">
        <h1>
          <i class="fa fa-square" style="font-size: inherit;"></i>
          <span style="font-weight: 500;">Met. Institutt</span>
        </h1>
        
        <div class="header--right">
          <ul>
            <li id="scroll--ouroffer">Siste måling <?php echo substr($nowtime, 10, -3); ?>: <span style="color: rgba(255,255,255,0.8);"><?php echo $nowtemp ?>°C</span></li>
          </ul>
        </div>
      </div>
      
      <div class="bigtext">
        <h2>
          Målingsdata fra blindern i oslo
        </h2>
      </div>
      
      <div id="scrollbtn" class="scrollcircle">
				<i class="fa fa-chevron-circle-down fa-5x" aria-hidden="true" style="color: white;"></i>
			</div>
    </div>
		
		<div class="page--apply" align="center">
      <div class="page--apply" align="center">
				<div class="uptime">
					<h1 align="center">
						TOTAL OPPETID<hr style="width: 50%;">
					</h1>
					<p align="center">
						<span style="font-size:40px;"><?php echo substr($uptime, 0, -10); ?>%</span>
					</p>
				</div>
			</div>
    </div>
		
    <div class="page--ouroffer" align="center">
			<div class="ab--block">
				<div class="container left">
          <div style="position: relative;">
            <h1 id="img--text">
							<a href="#modal" style="border: none; background: transparent; letter-spacing: 2px; color: white; font-size: 30px; text-transform: uppercase; text-decoration: none;">Grafer</a>
							
							<div class="remodal" data-remodal-id="modal">
								<button data-remodal-action="close" class="remodal-close"></button>
								<h1>Grafer</h1>
								<p>
									Graf over den siste timen
								</p>
								<canvas id="readings_Meas" style="width: 50vw; height: 500px;"></canvas>
								<br>
								<p>
									Graf over de siste 24 timene
								</p>
								<canvas id="readings_Meas_24h" style="width: 50vw; height: 500px;"></canvas>
								<br>
								<button data-remodal-action="confirm" class="remodal-confirm">OK</button>
							</div>
            </h1>
          </div>
        </div><div class="container right">
          <div style="position: relative;">
            <h1 id="img--text">
              DATA
            </h1>
          </div>
        </div>
			</div>
    </div>

		<hr>

		<div class="page--apply" align="center">
      <div class="page--apply" align="center">
				<div class="socials">
					<h1 align="center">
						Artikkel<hr style="width: 50%;">
					</h1>
					<p align="center">
						Artikkelen kommer her når den<br> er publisert
					</p>
				</div>
			</div>
    </div>
		<script>
			setInterval(ajaxCall, 30000); 

			function ajaxCall() {
				$.ajax({
				type: 'POST',
				url: 'get_1h.php',
				success: function (datai) {
				var ctx = document.getElementById("readings_Meas").getContext('2d');
				Chart.defaults.global.defaultFontColor = "black";
				var myLineChart = new Chart(ctx, {
						type: 'line',
						scaleFontColor: "#eee",
						data: (JSON.parse(datai)),
						options: {
								scales: {
										yAxes: [{
												ticks: {
														beginAtZero: false
												}
										}]
								}
						}
				});  
				} 
				});
					}
			
			
			setInterval(ajaxCall_24h, 30000);
    
			function ajaxCall_24h() {
			$.ajax({
			type: 'POST',
			url: 'get_24h.php',
			success: function (datai) {
			var ctx = document.getElementById("readings_Meas_24h").getContext('2d');
			Chart.defaults.global.defaultFontColor = "black";
			var myLineChart = new Chart(ctx, {
					type: 'line',
					scaleFontColor: "#eee",
					data: (JSON.parse(datai)),
					options: {
							scales: {
									yAxes: [{
											ticks: {
													beginAtZero: false
											}
									}]
							}
					}
			});  
			} 
			});
				}
			
			
    
			function ajaxCall_allTime() {
			$.ajax({
			type: 'POST',
			url: 'get_allTime.php',
			success: function (datai) {
			var ctx = document.getElementById("readings_Meas_allTime").getContext('2d');
			Chart.defaults.global.defaultFontColor = "black";
			var myLineChart = new Chart(ctx, {
					type: 'line',
					scaleFontColor: "#eee",
					data: (JSON.parse(datai)),
					options: {
							scales: {
									yAxes: [{
											ticks: {
													beginAtZero: false
											}
									}]
							}
					}
			});  
			} 
			});
				}
		</script>
  </body>
</html>