// use random() in a loop
// count how many samples are below 0.5
// sum generated samples and branch on the result

seed(0);

println(random()); // 0.8444218515250481
println(random()); // 0.7579544029403025

num low_count = 0;
num total = 0;

for i from 0 to 3 {
	num sample = i*random()+1; // 1.0, 1.2589167502929635, 2.0225494427372173

	println(sample);
}


println(seed());



// Expected output:
// 0.8444218515250481
// 0.7579544029403025
// 1
// 1.8444218515250481
// 2.7579544029403025
// 0

