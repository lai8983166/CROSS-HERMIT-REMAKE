
void __fastcall FUN__text__00410db0(int param_1)

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
  _memset((void *)(param_1 + 0xc),0,0x100);
  _memset((void *)(local_8 + 0x10c),0,0x14);
  _memset((void *)(local_8 + 0x380),0,0x534);
  _memset((void *)(local_8 + 0x8b4),0,300);
  FUN__text__00412b70(0x1e,2);
  FUN__text__00412c10(0x1e,2);
  *(int *)(local_8 + 0x8b4) = *(int *)(local_8 + 0x378) / 2;
  *(int *)(local_8 + 0x8b8) = *(int *)(local_8 + 0x37c) / 2;
  *(undefined4 *)(local_8 + 0x8bc) = 0;
  local_8 = 0x410e8a;
  FUN__text__0056ce80();
  return;
}

