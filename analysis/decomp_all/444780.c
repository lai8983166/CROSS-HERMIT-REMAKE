
void __fastcall FUN__text__00444780(int param_1)

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
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1c30),0,0x3700);
  local_8 = 0x4447c2;
  FUN__text__0056ce80();
  return;
}

