
void __thiscall FUN__text__0043d0c0(int param_1,void *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  size_t local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int)*(short *)(*(int *)(param_1 + 0x2659c) + 4) *
            (int)*(short *)(*(int *)(param_1 + 0x2659c) + 6);
  local_8 = param_1;
  _memset(param_2,0,local_c);
  local_8 = 0x43d11c;
  FUN__text__0056ce80();
  return;
}

