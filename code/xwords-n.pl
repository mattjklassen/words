my $n = shift(@ARGV);

my $input = join "", ($n, "sort.txt");

my $output = join "", ($n, "words.txt");

open(INPUT, $input) or 
          die "Can't open $input";

open(OUTPUT, "> $output") or
          die "Can't open $output";

my $previous = "";

until (eof(INPUT))
{
    my $line = <INPUT>;
    chomp $line;
    $alpha = substr($line,0,$n);
    if ($alpha eq $previous) {
        # print("found dup\n");
    }
    else {
        $previous = $line;
        print OUTPUT "$line\n";
    }
}

close OUTPUT;
close INPUT;

exit 0;
