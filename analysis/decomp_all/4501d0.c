
void __thiscall FUN__text__004501d0(int param_1,undefined4 param_2)

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
  FUN__text__0056d810(param_1 + 0x8e8,&DAT_00592b28,param_1 + 0xcf8,param_2);
  local_8 = 0x450227;
  FUN__text__0056ce80();
  return;
}

