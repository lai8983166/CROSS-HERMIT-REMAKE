
void __fastcall FUN__text__00432770(int param_1)

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
  if (*(int *)(param_1 + 0x2e6f4) == 0) {
    local_8 = param_1;
    FUN__text__004549d0(0,0,0,1,0,0,1);
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
  }
  local_8 = 0x4327db;
  FUN__text__0056ce80();
  return;
}

