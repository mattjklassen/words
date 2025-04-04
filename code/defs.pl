
$input = "engdict.txt";

$n = 13;

while ($n < 16) {

$output = "all.txt";

$output = "$n$output";

open(INPUT, $input) or 
          die "Can't open $input";

open(OUTPUT, "> $output") or
          die "Can't open $output";

until (eof(INPUT))
   {
	my $line = <INPUT>;
	chomp $line;
	my @parts = split(/\t/, $line);
	my $word = $parts[0];
	my @letters = split(//, $word);
	my $len = $#letters;
	if ($len == $n - 1)
	{
	   print OUTPUT "$line\n";
	}
    }

close OUTPUT;
close INPUT;

$n += 1;

}

exit 0;
