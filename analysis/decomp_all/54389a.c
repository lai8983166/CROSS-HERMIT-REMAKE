
int FUN__text__0054389a(char *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  char *pcVar4;
  
  iVar1 = FUN__text__0054bbd1(1);
  if (iVar1 == 0) {
    return 0;
  }
  iVar2 = __setjmp3(iVar1,0);
  if (iVar2 != 0) {
    FUN__text__0054bc56(iVar1,*(undefined4 *)(iVar1 + 0x9c));
    FUN__text__0054bc13(iVar1);
    return 0;
  }
  FUN__text__005437fb(iVar1,param_2,param_3,param_4);
  if ((param_1 == (char *)0x0) || (*param_1 != '1')) {
    FUN__text__0054381d(iVar1,"Incompatible libpng version in application and library");
  }
  *(undefined4 *)(iVar1 + 0xa0) = 0x2000;
  uVar3 = FUN__text__0054bc20(iVar1,0x2000);
  *(undefined4 *)(iVar1 + 0x9c) = uVar3;
  *(code **)(iVar1 + 0x84) = FUN__text__00546672;
  *(code **)(iVar1 + 0x88) = thunk_FUN__text__0054bc56;
  *(int *)(iVar1 + 0x8c) = iVar1;
  iVar2 = FUN__text__0054b70a(iVar1 + 100,"1.1.3",0x38);
  if (iVar2 == -6) {
    pcVar4 = "zlib version error";
  }
  else if ((iVar2 == -4) || (iVar2 == -2)) {
    pcVar4 = "zlib memory error";
  }
  else {
    if (iVar2 == 0) goto LAB__text__00543979;
    pcVar4 = "Unknown zlib error";
  }
  FUN__text__0054381d(iVar1,pcVar4);
LAB__text__00543979:
  *(undefined4 *)(iVar1 + 0x70) = *(undefined4 *)(iVar1 + 0x9c);
  *(undefined4 *)(iVar1 + 0x74) = *(undefined4 *)(iVar1 + 0xa0);
  FUN__text__005465a0(iVar1,0,0);
  return iVar1;
}

