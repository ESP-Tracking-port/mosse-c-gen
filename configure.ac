AC_INIT(MosseTables, 0.5)
AC_PREREQ(2.5)

dnl Look for python

AC_MSG_CHECKING(--with-python argument)
AC_ARG_WITH([python],
	[  --with-python           Use custom python interpreter],
	[with_python=$withval],
	[with_python=python3])
AC_MSG_RESULT($with_python)
AC_CHECK_PROGS(python, $with_python)
if test x$python = "x" ; then
	AC_MSG_ERROR([Cound not find python interpreter])
fi

AC_OUTPUT(Makefile)

