echo 1..$1

tmpdir=$(mktemp -d)
trap "rm -rf $tmpdir" EXIT

run_test()
{
    n=$1
    name=$2
    desc=$3
    $SHELL -e -c "
    rm -rf $tmpdir/{expected,actual}
    cp -a $(basename $0 .sh)/$name $tmpdir/expected
    ./common/run.sh $tmpdir/actual $(basename $0 .sh)/${name}.au3
    sed -i '/^ Generated:/d' $tmpdir/{expected,actual}/ublue_setup.gen.out.txt
    diff -Naur $tmpdir/{expected,actual}
    " >&2 && echo "ok $n - $desc" || echo "not ok $n - $desc"
}
