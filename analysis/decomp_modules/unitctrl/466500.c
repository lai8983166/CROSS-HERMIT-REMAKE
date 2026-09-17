
void __fastcall FUN__text__00466500(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_1 + 0x10c680;
  local_8 = param_1;
  _memset((void *)(param_1 + 0x10c680),0,0x3340);
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    *(undefined2 *)(local_10 + local_c * 0x520) = 1;
    *(undefined4 *)(local_10 + 0x44 + local_c * 0x520) = *(undefined4 *)(local_8 + 0x2a6e8);
    FUN__text__00409ef0(local_10 + 0x48 + local_c * 0x520);
  }
  local_8 = 0x4665b9;
  FUN__text__0056ce80();
  return;
}

