
$input = "engdict.txt";

$output = "2allnew.txt";

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
  	my $len = @letters;
  	if ($len == 2)
    { 
#  	    print OUTPUT "$line\n";
        print "$line\n";
        print "$word\n";
        print "@letters\n";
        print "$len\n";
  	}
}

close OUTPUT;
close INPUT;

exit 0;
