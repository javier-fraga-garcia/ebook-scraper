# Monitorización de Ofertas Diarias de Ebooks Kobo

Este proyecto utiliza una función Lambda de AWS escrita en Python para monitorizar las ofertas diarias de ebooks en Kobo. Los datos recopilados se procesan utilizando **dataclasses** de Python y se almacenan en una base de datos serverless (*DynamoDB*).

## Estructura del Repositorio

- `lambda_function.py` &rarr; archivo con la lógica de la función Lambda, incluyendo el código para realizar el scraping de las ofertas diarias.

- `CreateZip.ps1` &rarr; script de PowerShell que se encarga de comprimir las dependencias de Python y el archivo principal en una carpeta llamada **lambda_function.zip**, que se utiliza para implementar el proyecto en Lambda.

- `requirements.txt` &rarr; Contiene información sobre las dependencias necesarias para la correcta ejecución de la función.

## Configuración y Uso

1. **Configuración de AWS Lambda**: Asegúrate de tener una cuenta de AWS y configurado el entorno Lambda. Puedes seguir la [documentación oficial de AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) para obtener más información.

2. **Compresión de Dependencias**: Ejecuta el script `CreateZip.ps1` para comprimir las dependencias y el archivo principal en un archivo `lambda_function.zip`.

3. **Implementación en Lambda**: Carga el archivo `lambda_function.zip` en la consola de AWS Lambda para implementar la función.

4. **Configuración de políticas**: Para que la funcion Lambda pueda leer y escribir datos en DynamoDB es necesario añadir una política al rol de ejecución de la función. Se puede añadir utilizando el siguiente **JSON** cambiando el **ARN** del **Resource**:

```json
{
	"Version": "2012-10-17",
	"Statement": [{
			"Effect": "Allow",
			"Action": [
				"dynamodb:GetItem",
				"dynamodb:PutItem"
			],
			"Resource": "arn:aws:dynamodb:eu-west-1:123456789012:table/SampleTable"
		}
    ]
}
```

5. **Configuración de Eventos**: Configura eventos programados para ejecutar la función Lambda diariamente o según tus necesidades.

Para más información se pueden consultar los siguientes enlaces:

* [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* [Amazon DynamoDB](https://aws.amazon.com/es/dynamodb/)
* [How to Create an AWS IAM Policy to Grant AWS Lambda Access to an Amazon DynamoDB Table](https://aws.amazon.com/es/blogs/security/how-to-create-an-aws-iam-policy-to-grant-aws-lambda-access-to-an-amazon-dynamodb-table/)
