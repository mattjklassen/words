
$n = 2;

$input1 = "$n"."sort.txt";
$input2 = "engdict.txt";

$output = "4all.txt";

open(INPUT1, $input1) or 
          die "Can't open $input1";

open(INPUT2, $input2) or 
          die "Can't open $input2";

open(OUTPUT, "> $output") or
          die "Can't open $output";

# print "$input1\n";
# print "$input2\n";

until (eof(INPUT1))
   {
	my $line1 = <INPUT1>;
	chomp $line1;
	my @words = split(/,/, $line1);
	my $word = $words[0];
	my $match = 0;
	while ($match == 0) {
	   my $line2 = <INPUT2>;
	   chomp $line2;
	   my @parts = split(/,/, $line2);
	   my $comp = $parts[0];
	   if ($word =~ m/$comp/) {
		print "$line2\n";
		$match = 1;
	   }
	}
    }

close OUTPUT;
close INPUT1;
close INPUT2;

exit 0;
