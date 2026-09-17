
/* Library Function - Single Match
    ___lc_lctostr
   
   Library: Visual Studio 2003 Debug */

void ___lc_lctostr(undefined4 param_1,int param_2)

{
  FUN__text__0056cd90(param_1,param_2);
  if (*(char *)(param_2 + 0x40) != '\0') {
    __strcats(param_1,2,&DAT_00594bd8,param_2 + 0x40);
  }
  if (*(char *)(param_2 + 0x80) != '\0') {
    __strcats(param_1,2,&DAT_005c8218,param_2 + 0x80);
  }
  return;
}

