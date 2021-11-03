package main

import (
	"flag"
	"fmt"
	"os"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func main() {
	mode := flag.String("mode", "", "server mode")

	flag.Parse()

	fmt.Println(*mode)
	if *mode == "web" {
//		fmt.Println("Start web")
		startWeb()
	} else {
//		fmt.Println("Start lambda")
		startLambda()
	}
}

func startLambda() {
	lambda.Start(func(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusOK,
			Body: getContent(),
		}, nil
	})
}

func startWeb() {
	port := os.Getenv("port")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		switch request.URL.Path {
		default:
			writer.WriteHeader(http.StatusNotFound)
		case "/":
			_, _ = fmt.Fprint(writer, getContent())
		case "/health":
			writer.WriteHeader(http.StatusOK)
			_, _ = fmt.Fprint(writer, "healthy")
		}
	})
	_ = http.ListenAndServe(":" + port, nil)
}

func getContent() string {
	return "Hello, DevOps! v6"
}
