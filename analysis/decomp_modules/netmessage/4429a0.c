
void FUN__text__004429a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_94 [16];
  undefined4 local_54;
  int local_50;
  undefined1 local_4c [13];
  undefined1 local_3f;
  undefined1 auStack_3a [50];
  int local_8;
  
  puVar2 = local_94;
  for (iVar1 = 0x24; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(local_4c,0,0x44);
  local_3f = 7;
  for (local_50 = 0; local_50 != 4; local_50 = local_50 + 1) {
    auStack_3a[local_50] = *(undefined1 *)(local_8 + local_50 + 0x1a8c);
  }
  local_54 = FUN__text__00419fe0(local_4c,0x44);
  local_8 = 0x442a3d;
  FUN__text__0056ce80();
  return;
}

