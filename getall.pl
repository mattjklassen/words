
$input = "engdict.txt";

$n = 2;

while ($n < 6)
{

open(INPUT, $input) or 
          die "Can't open $input";

my $output = join "", ($n, "allnew.txt");

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
  	if ($len == $n)
    { 
  	    print OUTPUT "$line\n";
        print "$line\n";
#        print "$word\n";
#        print "@letters\n";
#        print "$len\n";
  	}
}

close OUTPUT;
close INPUT;

$n += 1;

} # end while ($n < 16)

exit 0;
