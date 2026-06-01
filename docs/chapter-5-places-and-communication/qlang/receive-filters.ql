place Sensor {
    num reading = 37;
    send reading to Hub as "temperature";
}

place Hub {
    // Filter by type, source, and name
    num temp = receive num from Sensor named "temperature";
    println("Temperature: %d" % temp);
}
