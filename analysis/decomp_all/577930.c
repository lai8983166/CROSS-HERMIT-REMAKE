
void FUN__text__00577930(int param_1,undefined4 *param_2)

{
  code *pcVar1;
  int iVar2;
  
  if (((param_1 != 0) && (param_1 != 1)) &&
     (iVar2 = FUN__text__00573780(2,"_sftbuf.c",0xa1,0,"flag == 0 || flag == 1"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((param_1 != 0) && ((param_2[3] & 0x1000) != 0)) {
    FUN__text__005775c0(param_2);
    param_2[3] = param_2[3] & 0xffffeeff;
    param_2[6] = 0;
    *param_2 = 0;
    param_2[2] = 0;
  }
  return;
}

