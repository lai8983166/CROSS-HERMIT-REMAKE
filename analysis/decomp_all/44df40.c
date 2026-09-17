
void __thiscall FUN__text__0044df40(int param_1,undefined2 param_2,undefined2 param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0xb0) = 0;
  *(undefined1 *)(param_1 + 0xbb) = 0xff;
  *(undefined1 *)(param_1 + 0xb8) = 0x80;
  *(undefined1 *)(param_1 + 0xb9) = 0x80;
  *(undefined1 *)(param_1 + 0xba) = 0x80;
  local_8 = param_1;
  FUN__text__0044e140(param_1 + 0x54,param_2,param_3,0x50,1,&DAT_006068b8 + param_4 * 8);
  local_8 = 0x44dfc7;
  FUN__text__0056ce80();
  return;
}

