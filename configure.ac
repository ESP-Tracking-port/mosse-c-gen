AC_INIT(MosseTables, 0.5)
AC_PREREQ(2.5)

dnl Look for python

AC_ARG_WITH(python,
	[--with-python, Use custom python interpreter],
	with_python=$python,
	with_python=python3)
AC_CHECK_PROGS(python, $python)
if test x$python = "x" ; then
	AC_MSG_ERROR([Cound not find python interpreter])
fi

AC_OUTPUT(Makefile)

