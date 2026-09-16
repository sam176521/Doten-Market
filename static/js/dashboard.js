document.addEventListener(
    "DOMContentLoaded",
    function(){


        function createChart(
            id,
            type,
            label
        ){

            const canvas =
                document.getElementById(id);


            if(!canvas)
                return;



            new Chart(canvas, {

                type:type,


                data:{

                    labels:JSON.parse(
                        canvas.dataset.labels
                    ),


                    datasets:[{

                        label:label,


                        data:JSON.parse(
                            canvas.dataset.values
                        ),


                        borderWidth:2

                    }]

                },


                options:{

                    responsive:true,


                    scales:{

                        y:{

                            beginAtZero:true

                        }

                    }

                }

            });

        }



        createChart(
            "ventesChart",
            "line",
            "Chiffre d'affaires"
        );


        createChart(
            "produitsChart",
            "bar",
            "Quantité vendue"
        );


        createChart(
            "stockChart",
            "doughnut",
            "Stock"
        );


    }
);