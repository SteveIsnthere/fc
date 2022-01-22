String x;

void myFunction()
{
    Serial.println("func ran");
}
void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(1);
}
void loop()
{
    while (!Serial.available())
    {
        x = Serial.readString();
        if (x[0] == '0')
        {
            myFunction();
        }
    }
}