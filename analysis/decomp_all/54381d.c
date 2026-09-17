
void FUN__text__0054381d(int *param_1,undefined4 param_2)

{
  if ((code *)param_1[0x10] != (code *)0x0) {
    (*(code *)param_1[0x10])(param_1,param_2);
  }
                    /* WARNING: Subroutine does not return */
  _longjmp(param_1,1);
}

