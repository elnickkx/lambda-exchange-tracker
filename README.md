# lambda-exchange-tracker

### Codebase for Lambda-based Currency Exchange application

---


> *  **_Backend Server: AWS Lambda - Serverless Infrastructure_**

- python3.11
- Curated requirements.in [basic dependency libs]
- Design Pattern followed: **_Creational-Singleton_** and **_Structural-Decorator_** Design Pattern
- Architecture: **_Event-Driven Asynchronous Architecture_**


### 1. Steps for executing and hosting of application locally

**Installation Guide for LocalStack support ecosystem**

```
Installation Guide: https://docs.localstack.cloud/getting-started/installation/
```

**Initiating the Localstack application server**

```
localstack start # initialize
```

### 2. To setup the required AWS services locally via IaC and CDK

```
sudo chmod +x run_executor.sh
Run the command: /bin/bash run_executor.sh
```

### 3. Login to LocalStack Web-App to visualize the initiated services


```
Navigate to: `https://app.localstack.cloud/dashboard`

```


### 4. Architectural Design - Business Logic

![img.png](img.png)

> * **_Cloudwatch EventBridge_**
>   * Event Rule defined to periodically trigger Lambda action to scrape the Currency Conversion (daily basis).
>   * Once scraped, evaulate the fluctuated spot rate for enlisted currency for exchange and stored as time-series documents (NoSQL schema).

> * **_API Gateway Resources_**
>   * Publically exposed **_GET_** method to fetch the **_Currency Spot Rate and Fluctuations_** for enlisted currencies.
>   * API Gateway service, being hosted on **_https://localhost.localstack.cloud:4566_** domain to emulate the AWS ecosystem.

### 5. Manual Modular Testing

> * As to perform **_Modular Testing_**, execute the inline command: **_python3 worker_lambda.py_**
>   * For EventBridge moderation: **_report_generation_cron_event_** as placeholder value
>   * For APIGateway moderation: **_api_currency_exchange_event_** as placeholder value
> * Code Snippet:
>   *     class Context:
            invoked_function_arn = "test:dev"

            print(
                async_lambda_handler(
                    event=events.api_currency_exchange_event, context=Context()
                )
            )

---

