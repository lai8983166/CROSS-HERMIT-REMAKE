
/* Library Function - Single Match
    __fassign
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2003 Release */

void __cdecl __fassign(int flag,char *argument,char *number)

{
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  if (flag == 0) {
    FUN__text__00585270(&local_10,number);
    *(undefined4 *)argument = local_10;
  }
  else {
    FUN__text__005851f0(&local_c,number);
    *(undefined4 *)argument = local_c;
    *(undefined4 *)(argument + 4) = local_8;
  }
  return;
}

