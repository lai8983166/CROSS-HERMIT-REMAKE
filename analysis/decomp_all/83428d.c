
undefined * FUN__text1__0083428d(void)

{
  ushort uVar1;
  int iVar2;
  undefined *puVar3;
  int iVar4;
  undefined *local_1c;
  int local_c;
  
  puVar3 = PTR_IMAGE_DOS_HEADER_008751e8;
  if (PTR_IMAGE_DOS_HEADER_008751e8 != (undefined *)0x0) {
    local_1c = PTR_IMAGE_DOS_HEADER_008751e8 + *(int *)(PTR_IMAGE_DOS_HEADER_008751e8 + 0x3c) + 0xf8
    ;
    uVar1 = *(ushort *)
             (PTR_IMAGE_DOS_HEADER_008751e8 + *(int *)(PTR_IMAGE_DOS_HEADER_008751e8 + 0x3c) + 6);
    for (local_c = 0; local_c < (int)(uint)uVar1; local_c = local_c + 1) {
      if (((*(uint *)(local_1c + 0x24) & 0x40000000) != 0) && (7 < *(uint *)(local_1c + 0x10))) {
        iVar2 = *(int *)(local_1c + 0xc);
        iVar4 = _memcmp(puVar3 + iVar2,"PDATA000",8);
        if (iVar4 == 0) {
          return puVar3 + iVar2;
        }
      }
      local_1c = local_1c + 0x28;
    }
  }
  return (undefined *)0x0;
}

