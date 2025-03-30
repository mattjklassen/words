
$input2 = "2sort.txt";
$input3 = "3sort.txt";

$output = "2-3-edges.txt";

open(INPUT2, $input2) or 
          die "Can't open $input2";
open(INPUT3, $input3) or 
          die "Can't open $input3";
open(OUTPUT, "> $output") or
          die "Can't open $output";

sub load_nodes
{
    my $m = $_[0];
    my $input = join "", ($m, "nodes.txt");
    print("$input\n");
    open(INPUT, $input) or
	    die "Can't open $input.";
    my @nodes = ();
    until (eof(INPUT))
    {
 	    my $line = <INPUT>;
 	    chomp $line;
	    push @nodes, $line;
    }
    close INPUT;
    return @nodes;
}

sub getunique
{
    my ($str) = @_;

    my @letters = split "", $str;
    my $let = ""; 
    my $temp = ""; 
    my $letter = ""; 
    my @lets = ();

    push @lets, $letters[0];

    foreach $letter (@letters)
    {
    	$dup = 0;
    	foreach $let (@lets)
    	{
    	    if ($let eq $letter)
    	    {
    		$dup = 1;
    	    }
    	}
    	if ($dup == 0)
    	{
    	    push @lets, $letter; 
    	}
    }
    @lets = sort @lets;
#   print "the distinct letters are: ", @lets, "\n";
    $temp = join "", @lets;
    return $temp;
}

sub getstrings
{
    my ($n, $str) = @_;
    my $tempstr = $str;
    my $letter = $str;
    my $remains = "";
    my @others = ();
    my $other = "";
    my $pair = "";
    my @out = ();

# need recursive call to get substrings of str with reps
# first get distinct letters from str, then do base case 2
# here we assume n at least two and length of string at least 2

    my $unique = getunique($str);
    my @list = split "", $unique;
# print "here is the list: ", @list, "\n";

    if ($n == 2)  # base case
    {
    	foreach my $letter (@list)
    	{
            $tempstr = $str;
            $tempstr =~ s/$letter//, $tempstr;
    	    $remains = getunique($tempstr);
    	    @others = split "", $remains;
    	    foreach $other (@others)
    	    {
    		    $pair = "$letter$other";
    		    push @out, $pair;
    	    }
    	}
    }
    else  # now the recursion case
    {
    	foreach  $letter (@list)
    	{
            $tempstr = $str;
            $tempstr =~ s/$letter//, $tempstr;
            my $k=$n-1;
    	    @others = getstrings($k,$tempstr);
    	    foreach $other (@others)
    	    {
    		    $pair = "$letter$other";
    		    push @out, $pair;
    	    }
    	}
    }
    return @out;
}

# Define an n-alpha to be an alphabetized string (with repetitions) of length n.
# A sub-(n-1)-alpha of a given n-alpha is an (n-1)-alpha formed from the n-alpha by
# deleting one character.  
#
# Finding edges from 2-nodes to 3-nodes:  This should be done by going through
# the list of 3-nodes and in each case forming the sub-2-alpha's.  This is
# quite simple, since ABC has 3 such (not 6, because half the perms are not
# alphabetized), and AAB has only two.  Each sub-2-alpha forms a 2-3-edge when 
# it is a 2-node, otherwise not.  That's it. The text file 2-3-edges.txt should
# have each 2-node followed by a ; and then the list of single letters separated
# by commas so that each letter represents a 2-3-edge.  

# The above applies to all formation of k-n edges with k=n-1.  The next case
# is k=n-2 with first example 2-4-edges.  This can begin with formation of
# 3-alphas from each 4-node, then 2-alphas from each of those 3-alphas.
# Each 4-node will produce at most 4 3-alphas and then at most 3 2-alphas, so
# a total of 12 2-alphas. Any 3-alpha which is a 3-node can be ignored, since
# each 2-node below it has a path to the 3-node. A 3-alpha which is not a 3-node
# might have a 2-alpha below it which is a 2-node. In this case we would need
# to check if such 2-node has any other path directly to a 3-node and then to
# the 4-node under consideration. If it does not, then it gives a 2-4-edge.
#
# Another way to describe this process is: for each 4-node, construct the
# tree with root this 4-node, and children are 3-alphas and leaves are the 2-alphas.  
# Make a list of the 2-alphas (no dups) and remove any that are not 2-nodes.
# If this list is empty then there are no 2-4-edges needed.  If not, then need
# to check each remaining 2-node and see if it occurs as a leaf under a 3-node.
# If it does not occur, then it needs a 2-4-edge. In the process of checking
# the 2-nodes in the list, one uses the tree described above.  This tree can
# be pruned (after forming the list) so that it contains only nodes (as opposed
# to alphas which are non-nodes).  

# The above process can be repeated for 3-5-edges. This depends on having formed
# the 3-4 and 4-5 edges already.  Then the 2-5 edges would be the next step. 
# For the 2-5-edges we can again construct the tree and the list as above for
# each 5-node.  Again the list of 2-nodes is checked for necessary 2-5-edges
# by working with the pruned tree under the 5-node.  This tree has only nodes
# (as opposed to alphas) and contains all edges of type 2-3, 3-4, 4-5, 2-4, 3-5,
# so that we can evaluate any potential 2-5-edge by checking for any other path
# from a 2-node in the list to the 5-node.  This pretty much describes the general
# case now, for finding k-n-edges, with k<n<16.  To do this we need to have the tree
# from any n-node with all paths down to (k+1)-nodes.  We then make the list of
# k-nodes in the usual way, and use the tree to check for necessary k-n-edges.
# The farther the distance between k and n, the fewer edges we expect to find.

sub get_subalphas(
{
    my ($str) = @_;
    @out = ();
    my $unique = getunique($str);
    my @list = split "", $unique;
	foreach  $letter (@list)
	{
        $tempstr = $str;
        $tempstr =~ s/$letter//, $tempstr;
        my $k=$n-1;
	    @others = getstrings($k,$tempstr);
	    foreach $other (@others)
	    {
		    $pair = "$letter$other";
		    push @out, $pair;
	    }
	}
}


sub isword
{
    my ($word,$dictref) = @_;
    my $low = 0; 
    my $high = @$dictref - 1;
    
    while ($low <= $high)
    {
	    my $try = int( ($low + $high) / 2 );
	    $low = $try + 1, next if $dictref->[$try] lt $word;
	    $high = $try - 1, next if $dictref->[$try] gt $word;
	    return 1;
    }
    return 0;
}


my @nodes2 = load_nodes(2);
my @nodes3 = load_nodes(3);

my @out1 = grep(/AA/, @nodes3);

foreach (@out1) {
    print "$_\n";
    $out = getunique($_);
    print "$out\n";
    @list = getstrings(2, $_);
    print "@list\n";
}

my $str = "AABBC";
print "$str\n";
my @out2 = getstrings(3, $str);
print "@out2\n";


#my @out2 = grep(/A/, @nodes3);
#@out2 = grep(/A/, @out2);

#foreach (@out2) {
#    print "$_\n";
#}

exit 0;

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
  	    print OUTPUT "$line\n";
        print "$line\n";
        print "$word\n";
        print "@letters\n";
        print "$len\n";
  	}
}

close OUTPUT;
close INPUT;

