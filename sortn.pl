my $n = shift(@ARGV);

my $input = join "", ($n, "all.txt");

my $output = join "", ($n, "sort.txt");

open(INPUT, $input) or 
          die "Can't open $input";

open(OUTPUT, "> $output") or
          die "Can't open $output";


until (eof(INPUT))
    {
	my $line = <INPUT>;
	chomp $line;
        $line = substr($line,0,$n);
	my @letters = split(//, $line);
        my @sorted = sort @letters;
        my $out = join "", @sorted;
	print OUTPUT "$out,$line\n";
    }

close OUTPUT;
close INPUT;

exit 0;
