
void FUN__text__0057a0d0(void)

{
  if (DAT_0080ab40 != 0) {
    (*API_KERNEL32_DLL_VirtualFree)
              (*(int *)(DAT_0080ab40 + 0xc) + DAT_0080ab34 * 0x8000,0x8000,0x4000);
    *(uint *)(DAT_0080ab40 + 8) =
         *(uint *)(DAT_0080ab40 + 8) | 0x80000000U >> ((byte)DAT_0080ab34 & 0x1f);
    *(undefined4 *)(*(int *)(DAT_0080ab40 + 0x10) + 0xc4 + DAT_0080ab34 * 4) = 0;
    *(char *)(*(int *)(DAT_0080ab40 + 0x10) + 0x43) =
         *(char *)(*(int *)(DAT_0080ab40 + 0x10) + 0x43) + -1;
    if (*(char *)(*(int *)(DAT_0080ab40 + 0x10) + 0x43) == '\0') {
      *(uint *)(DAT_0080ab40 + 4) = *(uint *)(DAT_0080ab40 + 4) & 0xfffffffe;
    }
    if ((*(int *)(DAT_0080ab40 + 8) == -1) && (1 < DAT_0080ab44)) {
      (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,*(undefined4 *)(DAT_0080ab40 + 0x10));
      FUN__text__005855a0(DAT_0080ab40,DAT_0080ab40 + 0x14,
                          (DAT_0080ab48 + DAT_0080ab44 * 0x14) - (DAT_0080ab40 + 0x14));
      DAT_0080ab44 = DAT_0080ab44 + -1;
    }
    DAT_0080ab40 = 0;
  }
  return;
}

